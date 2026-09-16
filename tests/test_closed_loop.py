"""Protocol and gate adversarial tests. All fixtures are synthetic and local."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "scripts" / "closed_loop.py"
SPEC = importlib.util.spec_from_file_location("closed_loop", SOURCE)
cl = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cl)


class Fixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.addCleanup(self.temp.cleanup)
        self.source = self.root / "implementation.txt"
        self.source.write_text("Synthetic implementation: two plus three equals five.\n", encoding="utf-8")
        self.contract = {"task_id": "SYNTH-001", "review_mode": "FULL", "open_decisions": [],
                         "minor_findings_block": True,
                         "acceptance_criteria": [{"id": "AC01", "criterion": "2 + 3 equals 5"}],
                         "required_evidence": ["EV01"]}

    def spec(self, paths=None):
        paths = paths or [self.source]
        return {"task_id": "SYNTH-001", "review_round": 1, "request_id": "REQ-SYNTH-R1",
                "destination": "synthetic-canonical-id", "purpose": "synthetic protocol test",
                "files": [{"path": str(p), "material_type": "source", "classification": "PUBLIC"} for p in paths],
                "authorization": {"approved": True, "destination": "synthetic-canonical-id",
                                  "purpose": "synthetic protocol test", "files": [str(p) for p in paths],
                                  "approval_evidence": "Synthetic fixture only; no external transmission."}}

    def bundle(self):
        return cl.prepare(self.spec())

    def review(self, bundle, status="PASS"):
        return {"message_type": "REVIEW_RESULT", "task_id": bundle["task_id"], "round": bundle["review_round"],
                "request_id": bundle["request_id"], "snapshot_id": bundle["snapshot_id"],
                "status": status, "summary": "Synthetic evidence inspected.", "findings": [], "missing_materials": [],
                "acceptance_criteria": [{"id": "AC01", "status": "PASS", "evidence": ["implementation.txt:1"]}],
                "architecture_direction": "CONTINUE", "ready_for_recheck": False}

    def readback(self, bundle, review=None):
        turns = [{"id": "synthetic-turn-%d" % i, "startedAt": 1000 + 10 * i, "completedAt": 1001 + 10 * i,
                  "status": "completed", "items": [{"type": "userMessage", "content": [{"type": "text", "text": text}]}]}
                 for i, text in enumerate(bundle["messages"])]
        if review is not None:
            turns[-1]["items"].append({"type": "agentMessage", "text": cl.canonical(review)})
        return {"pages": [{"thread": {"id": bundle["destination"], "kind": "chatgpt"}, "turns": turns}]}

    def save(self, name, value):
        path = self.root / name
        cl.write_json(path, value)
        return str(path)

    def evidence_record(self, path, evidence_id):
        return {"id": evidence_id, "path": path.name, "sha256": cl.digest(path.read_bytes())}

    def gate_fixture(self):
        output = self.root / "raw-output.txt"
        output.write_text("Synthetic test runner\nRan 1 test\nOK\n", encoding="utf-8")
        execution = self.root / "execution.json"
        command = "python3 synthetic_test.py"
        cl.write_json(execution, {"command": command, "cwd": str(self.root), "exit_code": 0,
                                  "output_sha256": cl.digest(output.read_bytes())})
        evidence = {"task_id": "SYNTH-001", "review_round": 1, "implementation_complete": True,
                    "implementation_summary": "Synthetic arithmetic fix.", "known_issues": [], "unverified_items": [], "open_decisions": [],
                    "artifacts": [self.evidence_record(output, "RAW"), self.evidence_record(execution, "EXEC")],
                    "commands": [{"id": "CMD", "command": command, "cwd": str(self.root), "exit_code": 0,
                                  "raw_output": "RAW", "execution_record": "EXEC"}],
                    "required_evidence_results": [{"id": "EV01", "status": "PASS", "evidence": ["CMD"]}],
                    "acceptance_results": [{"id": "AC01", "status": "PASS", "evidence": ["CMD"]}]}
        contract_path = self.save("contract.json", self.contract)
        evidence_path = self.save("evidence.json", evidence)
        bundle = cl.prepare(self.spec([self.source, Path(contract_path), Path(evidence_path), output, execution]))
        review = self.review(bundle)
        raw_message = cl.canonical(review)
        transcript = self.root / "internal-transcript.json"
        transcript.write_text("INDEPENDENT SYNTHETIC TEST FIXTURE\n" + raw_message, encoding="utf-8")
        internal = {"role": "internal_reviewer", "reviewer_id": "synthetic-independent-reviewer", "review": review,
                    "review_message": raw_message, "raw_transcript": {"path": transcript.name, "sha256": cl.digest(transcript.read_bytes())}}
        return {"run_root": str(self.root), "bundle": self.save("bundle.json", bundle), "contract": contract_path,
                "evidence": evidence_path, "implementer_id": "synthetic-implementer", "direction_reassessment_pending": False,
                "internal_review": self.save("internal.json", internal), "chatgpt_review": self.save("external.json", review),
                "readback": self.save("readback.json", self.readback(bundle, review))}

    def refresh_gate_snapshot(self, spec):
        old = cl.read_json(spec["bundle"])
        bundle = cl.prepare(self.spec([Path(r["source_file"]) for r in old["manifest"]["included"]]))
        review = self.review(bundle)
        cl.write_json(spec["bundle"], bundle)
        cl.write_json(spec["chatgpt_review"], review)
        cl.write_json(spec["readback"], self.readback(bundle, review))
        internal = cl.read_json(spec["internal_review"])
        internal["review"] = review
        internal["review_message"] = cl.canonical(review)
        transcript = self.root / internal["raw_transcript"]["path"]
        transcript.write_text("SYNTHETIC FIXTURE\n" + internal["review_message"], encoding="utf-8")
        internal["raw_transcript"]["sha256"] = cl.digest(transcript.read_bytes())
        cl.write_json(spec["internal_review"], internal)


class MaterialTests(Fixture):
    def test_I_long_payload_and_astral_envelope_budget(self):
        text = ('😀漢字\\"\n\t' * 6000) + "END"
        self.source.write_bytes(text.encode("utf-8"))
        bundle = self.bundle()
        parsed = cl.validate_bundle(bundle, current_files=True)
        parts = [m["content"] for m in parsed if m["MATERIAL"] == "M0001"]
        self.assertGreater(len(parts), 3)
        self.assertEqual("".join(parts), text)
        self.assertTrue(all(cl.units(m) <= 16000 for m in bundle["messages"]))
        self.assertEqual(bundle["manifest"]["included"][0]["checksum"], cl.digest(text))
        self.assertEqual(cl.verify_readback(bundle, self.readback(bundle))["status"], "PASS")

    def test_immutable_snapshot_is_deterministic_and_preserves_crlf(self):
        self.source.write_bytes(b"first\r\nsecond\n")
        a, b = self.bundle(), self.bundle()
        self.assertEqual(a, b)
        self.source.write_bytes(b"changed\n")
        self.assertIn("first\r\nsecond\n", json.loads(a["messages"][1])["content"])
        with self.assertRaises(cl.Invalid):
            cl.validate_bundle(a, current_files=True)

    def test_L_unapproved_file(self):
        spec = self.spec()
        extra = self.root / "business.txt"
        extra.write_text("Unapproved business material", encoding="utf-8")
        spec["files"].append({"path": str(extra), "material_type": "source", "classification": "PRIVATE"})
        with self.assertRaisesRegex(cl.Invalid, "Unauthorized"):
            cl.prepare(spec)

    def test_L_approval_is_exact_bool_destination_and_purpose(self):
        for field, value in (("approved", "true"), ("approved", 1), ("destination", "other"), ("purpose", "other")):
            with self.subTest(field=field, value=value):
                spec = self.spec()
                spec["authorization"][field] = value
                with self.assertRaises(cl.Invalid):
                    cl.prepare(spec)

    def test_L_symlink_scope_escape(self):
        link = self.root / "allowed-link.txt"
        link.symlink_to(self.source)
        with self.assertRaisesRegex(cl.Invalid, "symlink"):
            cl.prepare(self.spec([link]))

    def test_L_ancestor_symlink_scope_escape(self):
        real = self.root / "real"
        real.mkdir()
        path = real / "note.txt"
        path.write_text("test", encoding="utf-8")
        alias = self.root / "alias"
        alias.symlink_to(real, target_is_directory=True)
        with self.assertRaises(cl.Invalid):
            cl.prepare(self.spec([alias / "note.txt"]))

    def test_M_secret_values_inside_safe_filename(self):
        fixtures = ["sk-" + "A" * 40, "api_key=" + "A" * 24,
                    "-----BEGIN " + "PRIVATE KEY-----", "Authorization: Bearer " + "A" * 24,
                    "ghp_" + "b" * 40, "AKIA" + "A" * 16]
        for value in fixtures:
            with self.subTest(prefix=value[:5]):
                self.source.write_text("diff or log\n" + value, encoding="utf-8")
                with self.assertRaisesRegex(cl.Invalid, "secret"):
                    self.bundle()

    def test_M_quoted_json_yaml_and_toml_secret_assignments(self):
        fixtures = [json.dumps({"api_key": "A" * 24, "password": "B" * 24}),
                    "{!r}: {!r}".format("api-key", "A" * 24),
                    '"access_token" = "' + "B" * 24 + '"',
                    '"password":"' + "synthetic phrase" * 2 + '"',
                    '{"client_secret":"' + "C" * 10 + '!@#$%^&*"}']
        for value in fixtures:
            with self.subTest(format=value[:5]):
                self.source.write_text(value, encoding="utf-8")
                with self.assertRaisesRegex(cl.Invalid, "secret"):
                    self.bundle()

    def test_explicit_redacted_secret_placeholders_allowed(self):
        self.source.write_text(json.dumps({"api_key": "REDACTED", "password": "<removed locally>"}), encoding="utf-8")
        self.assertTrue(self.bundle()["messages"])

    def test_test_source_can_be_reviewed_without_literal_sensitive_values(self):
        source = Path(__file__).resolve()
        cl.safe_content(str(source), source.read_text(encoding="utf-8"), "PUBLIC")

    def test_M_env_filename_and_secret_classification(self):
        path = self.root / ".env"
        path.write_text("harmless=true", encoding="utf-8")
        with self.assertRaisesRegex(cl.Invalid, "filename"):
            cl.prepare(self.spec([path]))
        spec = self.spec()
        spec["files"][0]["classification"] = "SECRET"
        with self.assertRaisesRegex(cl.Invalid, "SECRET"):
            cl.prepare(spec)

    def test_sensitive_credential_directory(self):
        directory = self.root / ".ssh"
        directory.mkdir()
        path = directory / "config"
        path.write_text("test", encoding="utf-8")
        with self.assertRaises(cl.Invalid):
            cl.prepare(self.spec([path]))

    def test_non_utf8_image_rejected(self):
        self.source.write_bytes(bytes([137, 80, 78, 71, 255]))
        with self.assertRaisesRegex(cl.Invalid, "UTF-8"):
            self.bundle()

    def test_duplicate_source_rejected(self):
        spec = self.spec()
        spec["files"].append(copy.deepcopy(spec["files"][0]))
        with self.assertRaisesRegex(cl.Invalid, "Duplicate"):
            cl.prepare(spec)

    def test_oversized_control_envelope_rejected(self):
        spec = self.spec()
        spec["review_instructions"] = "😀" * 10000
        with self.assertRaisesRegex(cl.Invalid, "16000"):
            cl.prepare(spec)

    def test_secret_in_envelope_metadata_rejected(self):
        spec = self.spec()
        spec["purpose"] = "purpose " + "sk-" + "A" * 40
        spec["authorization"]["purpose"] = spec["purpose"]
        with self.assertRaisesRegex(cl.Invalid, "secret"):
            cl.prepare(spec)

    def test_tampered_pack_rejected(self):
        bundle = self.bundle()
        msg = json.loads(bundle["messages"][1])
        msg["content"] += "tamper"
        bundle["messages"][1] = cl.canonical(msg)
        with self.assertRaisesRegex(cl.Invalid, "checksum"):
            cl.validate_bundle(bundle)

    def test_tampered_manifest_rejected(self):
        bundle = self.bundle()
        bundle["manifest"]["included"][0]["checksum"] = "0" * 64
        with self.assertRaisesRegex(cl.Invalid, "snapshot"):
            cl.validate_bundle(bundle)


class ReadbackTests(Fixture):
    def test_J_stale_reply_materials_rejected(self):
        bundle = self.bundle()
        old = self.spec()
        old["review_round"] = 2
        old["request_id"] = "REQ-SYNTH-R2"
        with self.assertRaisesRegex(cl.Invalid, "Missing/old"):
            cl.verify_readback(bundle, self.readback(cl.prepare(old)))

    def test_K_queue_id_rejected(self):
        spec = self.spec()
        spec["destination"] = "local-chatgpt:synthetic"
        with self.assertRaisesRegex(cl.Invalid, "Canonical"):
            cl.prepare(spec)
        bundle = self.bundle()
        readback = self.readback(bundle)
        readback["pages"][0]["thread"]["id"] = "local-chatgpt:synthetic"
        with self.assertRaises(cl.Invalid):
            cl.verify_readback(bundle, readback)

    def test_wrong_kind_rejected(self):
        bundle = self.bundle()
        readback = self.readback(bundle)
        readback["pages"][0]["thread"]["kind"] = "codex"
        with self.assertRaisesRegex(cl.Invalid, "kind"):
            cl.verify_readback(bundle, readback)

    def test_missing_pack_rejected(self):
        bundle = self.bundle()
        readback = self.readback(bundle)
        readback["pages"][0]["turns"].pop(1)
        with self.assertRaisesRegex(cl.Invalid, "Missing"):
            cl.verify_readback(bundle, readback)

    def test_truncated_and_altered_message_rejected(self):
        bundle = self.bundle()
        readback = self.readback(bundle)
        readback["pages"][0]["turns"][1]["items"][0]["content"][0]["truncated"] = True
        with self.assertRaisesRegex(cl.Invalid, "truncated"):
            cl.verify_readback(bundle, readback)
        readback = self.readback(bundle)
        item = readback["pages"][0]["turns"][1]["items"][0]
        msg = json.loads(item["content"][0]["text"])
        msg["content"] = "altered"
        item["content"][0]["text"] = cl.canonical(msg)
        with self.assertRaisesRegex(cl.Invalid, "altered"):
            cl.verify_readback(bundle, readback)

    def test_overlapping_page_duplicate_is_idempotent_but_conflict_rejected(self):
        bundle = self.bundle()
        readback = self.readback(bundle)
        readback["pages"].append(copy.deepcopy(readback["pages"][0]))
        self.assertEqual(cl.verify_readback(bundle, readback)["status"], "PASS")
        item = readback["pages"][1]["turns"][1]["items"][0]
        msg = json.loads(item["content"][0]["text"])
        msg["snapshot_id"] = "f" * 64
        item["content"][0]["text"] = cl.canonical(msg)
        with self.assertRaisesRegex(cl.Invalid, "conflicting"):
            cl.verify_readback(bundle, readback)

    def test_materials_only_barrier(self):
        bundle = self.bundle()
        readback = self.readback(bundle)
        readback["pages"][0]["turns"].pop()
        self.assertEqual(cl.verify_readback(bundle, readback, True)["status"], "PACKS_VERIFIED")
        with self.assertRaises(cl.Invalid):
            cl.verify_readback(bundle, readback)

    def test_actual_tool_wrapper_supported(self):
        bundle = self.bundle()
        readback = self.readback(bundle)
        readback["pages"] = [{"content": [{"type": "text", "text": cl.canonical(readback["pages"][0])}]}]
        self.assertEqual(cl.verify_readback(bundle, readback)["status"], "PASS")

    def test_complete_before_materials_cannot_be_repaired_by_later_packets(self):
        bundle = self.bundle()
        readback = self.readback(bundle)
        turns = readback["pages"][0]["turns"]
        turns[-1]["startedAt"] = turns[0]["startedAt"] + 1
        turns[-1]["completedAt"] = turns[0]["startedAt"] + 2
        readback["pages"][0]["page"] = {"order": "newest_first"}
        readback["pages"][0]["turns"] = sorted(turns, key=lambda t: t["startedAt"], reverse=True)
        with self.assertRaisesRegex(cl.Invalid, "precedes material"):
            cl.verify_readback(bundle, readback)

    def test_unknown_chronology_is_not_assumed_success(self):
        bundle = self.bundle()
        readback = self.readback(bundle)
        del readback["pages"][0]["turns"][1]["startedAt"]
        with self.assertRaisesRegex(cl.Invalid, "chronology"):
            cl.verify_readback(bundle, readback)

    def test_turn_level_truncation_rejected(self):
        bundle = self.bundle()
        readback = self.readback(bundle)
        readback["pages"][0]["turns"][-1]["truncated"] = True
        with self.assertRaisesRegex(cl.Invalid, "truncated"):
            cl.verify_readback(bundle, readback)

    def test_newest_first_pages_use_actual_time_not_array_position(self):
        bundle = self.bundle()
        readback = self.readback(bundle)
        readback["pages"][0]["page"] = {"order": "newest_first"}
        readback["pages"][0]["turns"].reverse()
        self.assertEqual(cl.verify_readback(bundle, readback)["status"], "PASS")


class ReviewTests(Fixture):
    def test_valid_pass(self):
        bundle = self.bundle()
        self.assertEqual(cl.validate_review(self.review(bundle), self.contract, bundle)["status"], "VALID")

    def test_E_referenced_missing_requires_blocked(self):
        spec = self.spec()
        spec["referenced_but_not_included"] = [{"name": "03-schema.md", "reason": "Not authorized"}]
        bundle = cl.prepare(spec)
        review = self.review(bundle)
        with self.assertRaisesRegex(cl.Invalid, "BLOCKED"):
            cl.validate_review(review, self.contract, bundle)
        review.update(status="BLOCKED", missing_materials=["03-schema.md: not provided"])
        review["acceptance_criteria"][0].update(status="NOT_VERIFIED", evidence=[])
        self.assertEqual(cl.validate_review(review, self.contract, bundle)["review_status"], "BLOCKED")

    def test_schema_missing_fields_and_boolean_types(self):
        bundle = self.bundle()
        for key in self.review(bundle):
            with self.subTest(missing=key):
                review = self.review(bundle)
                del review[key]
                with self.assertRaises(cl.Invalid):
                    cl.validate_review(review, self.contract, bundle)
        for value in ("false", 0, [], None):
            review = self.review(bundle)
            review["ready_for_recheck"] = value
            with self.assertRaises(cl.Invalid):
                cl.validate_review(review, self.contract, bundle)

    def test_missing_duplicate_or_unknown_ac_rejected(self):
        bundle = self.bundle()
        for results in ([], [{"id": "other", "status": "PASS", "evidence": ["file:1"]}],
                        self.review(bundle)["acceptance_criteria"] * 2):
            review = self.review(bundle)
            review["acceptance_criteria"] = results
            with self.assertRaises(cl.Invalid):
                cl.validate_review(review, self.contract, bundle)

    def test_stale_review_binding_rejected(self):
        bundle = self.bundle()
        for key, value in (("round", 2), ("round", True), ("request_id", "old"), ("snapshot_id", "0" * 64)):
            review = self.review(bundle)
            review[key] = value
            with self.assertRaises(cl.Invalid):
                cl.validate_review(review, self.contract, bundle)

    def test_D_pass_without_evidence_rejected(self):
        bundle = self.bundle()
        review = self.review(bundle)
        review["acceptance_criteria"][0]["evidence"] = []
        with self.assertRaisesRegex(cl.Invalid, "evidence"):
            cl.validate_review(review, self.contract, bundle)

    def test_pass_blocking_finding_or_direction_rejected(self):
        bundle = self.bundle()
        finding = {"id": "F01", "severity": "MAJOR", "category": "correctness", "claim": "Wrong arithmetic",
                   "evidence": ["implementation.txt:1"], "reasoning": "Expected sum differs", "required_change": "Fix sum",
                   "verification_method": "Run test"}
        review = self.review(bundle)
        review["findings"] = [finding]
        with self.assertRaisesRegex(cl.Invalid, "blocking"):
            cl.validate_review(review, self.contract, bundle)
        review = self.review(bundle)
        review["architecture_direction"] = "STOP_AND_RETHINK"
        with self.assertRaisesRegex(cl.Invalid, "direction"):
            cl.validate_review(review, self.contract, bundle)


class GateTests(Fixture):
    def test_positive_full_gate_is_ready_not_user_accepted(self):
        result = cl.gate(self.gate_fixture())
        self.assertEqual(result["status"], "READY_FOR_USER_ACCEPTANCE")
        self.assertIs(result["user_accepted"], False)

    def test_N_external_fail_closes_gate(self):
        spec = self.gate_fixture()
        review = cl.read_json(spec["chatgpt_review"])
        review["status"] = "FAIL"
        review["acceptance_criteria"][0]["status"] = "FAIL"
        cl.write_json(spec["chatgpt_review"], review)
        with self.assertRaisesRegex(cl.Invalid, "not PASS"):
            cl.gate(spec)

    def test_D_claim_without_execution_record_rejected_after_fresh_review(self):
        spec = self.gate_fixture()
        evidence = cl.read_json(spec["evidence"])
        del evidence["commands"][0]["execution_record"]
        cl.write_json(spec["evidence"], evidence)
        self.refresh_gate_snapshot(spec)
        with self.assertRaisesRegex(cl.Invalid, "execution record"):
            cl.gate(spec)

    def test_nonbool_truthy_implementation_claim_rejected(self):
        for value in ("true", 1, [True]):
            spec = self.gate_fixture()
            evidence = cl.read_json(spec["evidence"])
            evidence["implementation_complete"] = value
            cl.write_json(spec["evidence"], evidence)
            self.refresh_gate_snapshot(spec)
            with self.assertRaisesRegex(cl.Invalid, "boolean"):
                cl.gate(spec)

    def test_empty_required_or_ac_coverage_rejected(self):
        for key in ("acceptance_results", "required_evidence_results", "artifacts"):
            spec = self.gate_fixture()
            evidence = cl.read_json(spec["evidence"])
            evidence[key] = []
            cl.write_json(spec["evidence"], evidence)
            self.refresh_gate_snapshot(spec)
            with self.assertRaises(cl.Invalid):
                cl.gate(spec)

    def test_bool_exit_code_rejected(self):
        spec = self.gate_fixture()
        evidence = cl.read_json(spec["evidence"])
        evidence["commands"][0]["exit_code"] = False
        cl.write_json(spec["evidence"], evidence)
        self.refresh_gate_snapshot(spec)
        with self.assertRaisesRegex(cl.Invalid, "command did not pass"):
            cl.gate(spec)

    def test_raw_output_execution_record_mismatch_rejected(self):
        spec = self.gate_fixture()
        evidence = cl.read_json(spec["evidence"])
        execution = self.root / "execution.json"
        record = cl.read_json(execution)
        record["output_sha256"] = "0" * 64
        cl.write_json(execution, record)
        evidence["artifacts"][1]["sha256"] = cl.digest(execution.read_bytes())
        cl.write_json(spec["evidence"], evidence)
        self.refresh_gate_snapshot(spec)
        with self.assertRaisesRegex(cl.Invalid, "Raw output differs"):
            cl.gate(spec)

    def test_real_empty_command_output_allowed_with_explicit_kind(self):
        spec = self.gate_fixture()
        evidence = cl.read_json(spec["evidence"])
        output = self.root / "raw-output.txt"
        output.write_bytes(b"")
        evidence["artifacts"][0].update(sha256=cl.digest(b""), kind="raw_output")
        execution = self.root / "execution.json"
        record = cl.read_json(execution)
        record["output_sha256"] = cl.digest(b"")
        cl.write_json(execution, record)
        evidence["artifacts"][1]["sha256"] = cl.digest(execution.read_bytes())
        cl.write_json(spec["evidence"], evidence)
        self.refresh_gate_snapshot(spec)
        self.assertEqual(cl.gate(spec)["status"], "READY_FOR_USER_ACCEPTANCE")

    def test_direct_light_never_claim_external_gate_support(self):
        for mode in ("DIRECT", "LIGHT"):
            spec = self.gate_fixture()
            contract = cl.read_json(spec["contract"])
            contract["review_mode"] = mode
            cl.write_json(spec["contract"], contract)
            with self.assertRaisesRegex(cl.Invalid, "FULL only"):
                cl.gate(spec)

    def test_tests_passed_claim_has_no_raw_output(self):
        spec = self.gate_fixture()
        (self.root / "raw-output.txt").unlink()
        with self.assertRaises(cl.Invalid):
            cl.gate(spec)

    def test_current_file_change_invalidates_old_pass(self):
        spec = self.gate_fixture()
        self.source.write_text("changed after review", encoding="utf-8")
        with self.assertRaisesRegex(cl.Invalid, "changed"):
            cl.gate(spec)

    def test_external_claim_not_in_agent_message_rejected(self):
        spec = self.gate_fixture()
        readback = cl.read_json(spec["readback"])
        readback["pages"][0]["turns"][-1]["items"].pop()
        cl.write_json(spec["readback"], readback)
        with self.assertRaisesRegex(cl.Invalid, "agentMessage"):
            cl.gate(spec)

    def test_external_pass_in_user_message_rejected(self):
        spec = self.gate_fixture()
        readback = cl.read_json(spec["readback"])
        item = readback["pages"][0]["turns"][-1]["items"][-1]
        item.update(type="userMessage", content=[{"type": "text", "text": item.pop("text")}])
        cl.write_json(spec["readback"], readback)
        with self.assertRaisesRegex(cl.Invalid, "agentMessage"):
            cl.gate(spec)

    def test_premature_review_before_material_complete_rejected(self):
        spec = self.gate_fixture()
        readback = cl.read_json(spec["readback"])
        reply = readback["pages"][0]["turns"][-1]["items"].pop()
        readback["pages"][0]["turns"][0]["items"].append(reply)
        cl.write_json(spec["readback"], readback)
        with self.assertRaisesRegex(cl.Invalid, "barrier"):
            cl.gate(spec)

    def test_gate_rejects_pass_before_materials_even_when_packets_later_complete(self):
        spec = self.gate_fixture()
        readback = cl.read_json(spec["readback"])
        turns = readback["pages"][0]["turns"]
        turns[-1].update(startedAt=1001, completedAt=1002)
        cl.write_json(spec["readback"], readback)
        with self.assertRaisesRegex(cl.Invalid, "precedes material"):
            cl.gate(spec)

    def test_repeated_identical_complete_accepts_only_later_valid_reply(self):
        spec = self.gate_fixture()
        readback = cl.read_json(spec["readback"])
        turns = readback["pages"][0]["turns"]
        later = copy.deepcopy(turns[-1])
        later["id"] = "synthetic-later-valid-complete"
        turns[-1].update(startedAt=1001, completedAt=1002)
        turns.append(later)
        # Both have identical JSON PASS; only the later chronological barrier counts.
        readback["pages"][0]["turns"].reverse()
        cl.write_json(spec["readback"], readback)
        self.assertEqual(cl.gate(spec)["status"], "READY_FOR_USER_ACCEPTANCE")

    def test_later_complete_without_its_own_pass_cannot_rescue_earlier_pass(self):
        spec = self.gate_fixture()
        readback = cl.read_json(spec["readback"])
        turns = readback["pages"][0]["turns"]
        later = copy.deepcopy(turns[-1])
        later["id"] = "synthetic-later-complete-without-review"
        later["items"].pop()
        turns[-1].update(startedAt=1001, completedAt=1002)
        turns.append(later)
        cl.write_json(spec["readback"], readback)
        with self.assertRaisesRegex(cl.Invalid, "valid MATERIAL_COMPLETE barrier"):
            cl.gate(spec)

    def test_review_completed_at_required(self):
        spec = self.gate_fixture()
        readback = cl.read_json(spec["readback"])
        del readback["pages"][0]["turns"][-1]["completedAt"]
        cl.write_json(spec["readback"], readback)
        with self.assertRaisesRegex(cl.Invalid, "completedAt"):
            cl.gate(spec)

    def test_internal_self_review_rejected(self):
        spec = self.gate_fixture()
        internal = cl.read_json(spec["internal_review"])
        internal["reviewer_id"] = spec["implementer_id"]
        cl.write_json(spec["internal_review"], internal)
        with self.assertRaisesRegex(cl.Invalid, "Independent"):
            cl.gate(spec)

    def test_internal_boolean_alone_rejected(self):
        spec = self.gate_fixture()
        cl.write_json(spec["internal_review"], {"internal_review_pass": True})
        with self.assertRaises(cl.Invalid):
            cl.gate(spec)

    def test_raw_internal_transcript_missing_rejected(self):
        spec = self.gate_fixture()
        (self.root / "internal-transcript.json").unlink()
        with self.assertRaises(cl.Invalid):
            cl.gate(spec)

    def test_pending_direction_reassessment_rejected(self):
        spec = self.gate_fixture()
        for value in (True, "false", 0, None):
            spec["direction_reassessment_pending"] = value
            with self.assertRaisesRegex(cl.Invalid, "Direction"):
                cl.gate(spec)

    def test_evidence_symlink_escape_rejected(self):
        spec = self.gate_fixture()
        path = self.root / "internal-transcript.json"
        original = path.read_bytes()
        external = self.root.parent / (self.root.name + "-outside.txt")
        self.addCleanup(lambda: external.unlink(missing_ok=True))
        external.write_bytes(original)
        path.unlink()
        path.symlink_to(external)
        with self.assertRaisesRegex(cl.Invalid, "escapes"):
            cl.gate(spec)


if __name__ == "__main__":
    unittest.main(verbosity=2)
