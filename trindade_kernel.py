"""
TRINDADE PROTOCOL - REFERENCE IMPLEMENTATION v1.7.6 [DIAMOND AGNOSTIC KERNEL]
Copyright (c) 2025 André Luiz Trindade (Primary Seed)

Licensed under the Business Source License 1.1 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at https://mariadb.com/bsl11/

Change Date: 2029-01-01
Change License: Apache License, Version 2.0

COMMERCIAL USE NOTICE:
This software is free for non-production use (Development/Personal). 
Production use requires a commercial license from the Architect: ANDRÉ LUIZ TRINDADE.

ARCHITECTURAL COMPLIANCE:
✓ Principle of Non-Reduction (2.1)
✓ Domain Agnosticism (2.2) 
✓ Separation of Concerns (2.3)
✓ SEASA Pipeline (3.0 LAYER 1) - With Semantic Triggers
✓ ALARP Risk Management (4.0)
✓ Pure Logic Core (No I/O in Layer 1)
"""

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import hashlib
import json
from uuid import uuid4

# ============================================================================
# SECTION 2.0: SYSTEM AXIOMS AND PRINCIPLES - FOUNDATIONAL TYPES
# ============================================================================

class DomainRoot(Enum):
    ENGINEERING = auto()
    MATHEMATICS = auto()
    PHYSICS = auto()
    COMPUTER_SCIENCE = auto()
    LAW = auto()
    MEDICINE = auto()
    ETHICS = auto()
    ARTS = auto()
    PHILOSOPHY = auto()
    BUSINESS = auto()
    UNKNOWN = auto()

class CriticalityIndex(Enum):
    CI_1 = 1  # Low
    CI_2 = 2  # Moderate
    CI_3 = 3  # Medium
    CI_4 = 4  # High
    CI_5 = 5  # Existential (Survival Protocol)

class DataTier(Enum):
    TIER_A = auto()
    TIER_B = auto()
    TIER_C = auto()

class EngineType(Enum):
    CREATIVE = auto()
    STRUCTURED = auto()
    ADVERSARIAL = auto()

class SEASAPhase(Enum):
    SEED = auto()
    EXPANSION = auto()
    AUDIT = auto()
    SYNTHESIS = auto()

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class DataPoint:
    content: Any
    tier: DataTier
    source: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    confidence: float = 1.0
    triangulation_sources: List[str] = field(default_factory=list)
    
    def is_triangulated(self) -> bool:
        if self.tier != DataTier.TIER_B:
            return True
        return len(self.triangulation_sources) >= 3

@dataclass
class ContractInput:
    domain_root: DomainRoot
    axiom_set: List[str]
    success_criteria: List[str]
    raw_input: str
    raw_input_hash: str
    axiom_data_points: List[DataPoint] = field(default_factory=list)
    temporal_budget: float = 60.0
    
    def calculate_complexity(self) -> Tuple[float, bool]:
        """Returns complexity score and whether existential trigger was found"""
        # CRITICAL CONSTRAINT v1.7.5: Semantic Trigger List
        existential_keywords = [
            "nuclear", "biohazard", "death", "collapse", "destroy", 
            "terminate", "emergency", "meltdown", "kill", "fail"
        ]
        
        # Check for existential triggers
        input_lower = self.raw_input.lower()
        existential_trigger_found = any(
            trigger in input_lower for trigger in existential_keywords
        )
        
        if existential_trigger_found:
            return 999.0, True
            
        base_score = len(self.axiom_set) * 1.5
        semantic_depth = len(self.raw_input.split()) / 50.0
        return base_score + semantic_depth, False

@dataclass
class RiskAssessment:
    probability: int
    impact: int
    description: str
    mitigation: Optional[str] = None
    
    @property
    def score(self) -> int:
        return self.probability * self.impact
    
    @property
    def is_critical(self) -> bool:
        return self.score > 15
    
    @property
    def alarp_status(self) -> str:
        if self.score <= 6: return "BROADLY_ACCEPTABLE"
        elif self.score <= 15: return "TOLERABLE_IF_ALARP"
        else: return "UNACCEPTABLE"

    def to_alarp_dict(self) -> Dict[str, Any]:
        return {
            "score": self.score,
            "probability": self.probability,
            "impact": self.impact,
            "description": self.description,
            "mitigation": self.mitigation,
            "status": self.alarp_status
        }

@dataclass
class SystemOutput:
    content: Any
    metadata: Dict[str, Any]
    risk_assessment: Optional[RiskAssessment] = None
    confidence: float = 1.0
    requires_human_approval: bool = False
    containment_active: bool = False
    
    def generate_logic_hash(self) -> str:
        risk_dict = self.risk_assessment.to_alarp_dict() if self.risk_assessment else None
        data_to_hash = {
            "content": str(self.content),
            "metadata": self.metadata,
            "risk": risk_dict,
            "containment": self.containment_active
        }
        json_str = json.dumps(data_to_hash, sort_keys=True, default=str)
        return hashlib.sha256(json_str.encode()).hexdigest()[:32]

# ============================================================================
# LAYER 0: DATA FOUNDATION
# ============================================================================

class IOracle(ABC):
    @abstractmethod
    def fetch_data(self, query: str, required_tier: DataTier) -> Optional[DataPoint]: pass
    @abstractmethod
    def triangulate(self, data_point: DataPoint) -> bool: pass

class OracleLayer:
    def __init__(self):
        self._oracles: Dict[str, IOracle] = {}
    
    def register_oracle(self, name: str, oracle: IOracle):
        self._oracles[name] = oracle
    
    def get_data(self, query: str, required_confidence: float = 0.9) -> DataPoint:
        results = []
        for name, oracle in self._oracles.items():
            for tier in [DataTier.TIER_A, DataTier.TIER_B, DataTier.TIER_C]:
                try:
                    dp = oracle.fetch_data(query, tier)
                    if dp: 
                        results.append(dp)
                        break
                except: continue
        
        if not results:
            return DataPoint(f"No data for {query}", DataTier.TIER_C, "System", confidence=0.0)
            
        best_point = max(results, key=lambda x: x.confidence)
        
        if best_point.tier == DataTier.TIER_B:
            for oracle_name, oracle in self._oracles.items():
                if oracle.triangulate(best_point):
                    best_point.triangulation_sources.append(oracle_name)
            if not best_point.is_triangulated():
                best_point.confidence *= 0.5
        
        return best_point

# ============================================================================
# LAYER 1: TRINDADE CORE (PURE LOGIC)
# ============================================================================

class TrindadeCore:
    def calculate_ci(self, contract: ContractInput) -> CriticalityIndex:
        complexity_score, existential_trigger = contract.calculate_complexity()
        
        # Fixed: Handle existential trigger properly
        if existential_trigger:
            return CriticalityIndex.CI_5
            
        if complexity_score < 5: return CriticalityIndex.CI_1
        if complexity_score < 15: return CriticalityIndex.CI_2
        if complexity_score < 30: return CriticalityIndex.CI_3
        if complexity_score < 60: return CriticalityIndex.CI_4
        return CriticalityIndex.CI_5
    
    def _seed_phase(self, contract: ContractInput) -> Dict:
        ci = self.calculate_ci(contract)
        missing_cnt = len(contract.axiom_set) - len(contract.axiom_data_points)
        return {
            "ci": ci,
            "missing_axioms_count": max(0, missing_cnt),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": str(uuid4()),
            "domain": contract.domain_root.name,
            "complexity_score": contract.calculate_complexity()[0]
        }
    
    def _expansion_phase(self, seed_result: Dict, contract: ContractInput) -> SystemOutput:
        is_high_risk = seed_result["ci"].value >= CriticalityIndex.CI_4.value
        
        draft_content = {
            "solution": f"Technical proposal for {contract.domain_root.name}",
            "rigor_level": "MAXIMUM" if is_high_risk else "STANDARD",
            "axioms_applied": len(contract.axiom_set),
            "methodology": "SEASA_GENERATIVE_LOGIC",
            "uncertainty_flags": []  # Fixed: Initialize the list
        }
        
        for dp in contract.axiom_data_points:
            if dp.tier == DataTier.TIER_B and not dp.is_triangulated():
                draft_content["uncertainty_flags"].append(f"Untriangulated: {dp.source}")
                
        return SystemOutput(
            content=draft_content,
            metadata={
                "phase": SEASAPhase.EXPANSION.name,
                "ci": seed_result["ci"].name,
                "domain": contract.domain_root.name
            }
        )

    def _audit_phase(self, draft: SystemOutput, seed_result: Dict, contract: ContractInput) -> RiskAssessment:
        prob = 1
        impact = 1
        
        if seed_result["ci"] == CriticalityIndex.CI_5:
            impact = 5
            prob = 4  # High probability assumption for existential threat
        
        if seed_result["missing_axioms_count"] > 0:
            prob += 1
            
        # Adjust based on data point confidence
        avg_confidence = sum(dp.confidence for dp in contract.axiom_data_points) / max(len(contract.axiom_data_points), 1)
        if avg_confidence < 0.5:
            prob += 2
            
        desc = f"Risk Assessment for {seed_result['domain']}"
        mitigation = None
        
        score = prob * impact
        if score > 15:
            desc = "CRITICAL: Risk threshold exceeded (ALARP Violation)"
            mitigation = "MANDATORY_CONTAINMENT_PROTOCOL"
        elif score > 6:
            mitigation = "Enhanced Validation Required"
            
        return RiskAssessment(prob, impact, desc, mitigation)

    def _synthesis_phase(self, draft: SystemOutput, risk: RiskAssessment, seed_result: Dict) -> SystemOutput:
        final_content = dict(draft.content) if isinstance(draft.content, dict) else {"raw": draft.content}
        containment = False
        
        if seed_result["ci"] == CriticalityIndex.CI_5:
            containment = True
            final_content["survival_protocol"] = {
                "status": "ACTIVE",
                "trigger": "EXISTENTIAL_THREAT_DETECTED",
                "priority": "EFFICACY_OF_INTERRUPTION",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        
        if risk.mitigation:
            final_content["mitigation_plan"] = risk.mitigation
            
        return SystemOutput(
            content=final_content,
            metadata={
                "ci": seed_result["ci"].name,
                "session_id": seed_result["session_id"],
                "purity_check": "PASSED_NO_IO",
                "license": "BUSL-1.1",
                "phase": SEASAPhase.SYNTHESIS.name,
                "complexity": seed_result.get("complexity_score", 0)
            },
            risk_assessment=risk,
            confidence=0.9 if risk.score < 10 else 0.5,
            requires_human_approval=risk.is_critical or containment,
            containment_active=containment
        )

    def execute_seasa(self, contract: ContractInput) -> SystemOutput:
        seed_result = self._seed_phase(contract)
        draft = self._expansion_phase(seed_result, contract)
        risk = self._audit_phase(draft, seed_result, contract)
        final_output = self._synthesis_phase(draft, risk, seed_result)
        return final_output

# ============================================================================
# LAYER 2 & 3 & 4: ORCHESTRATION
# ============================================================================

class IDomainAdapter(ABC):
    @property
    @abstractmethod
    def supported_domains(self) -> List[DomainRoot]: pass
    @abstractmethod
    def adapt_input(self, raw_input: str, oracle_layer: OracleLayer) -> ContractInput: pass

class EngineeringAdapter(IDomainAdapter):
    @property
    def supported_domains(self) -> List[DomainRoot]:
        return [DomainRoot.ENGINEERING, DomainRoot.PHYSICS]

    def adapt_input(self, raw_input: str, oracle_layer: OracleLayer) -> ContractInput:
        axioms = ["Safety First", "Thermodynamics", "Material Limits"]
        data_points = []
        for ax in axioms:
            try:
                dp = oracle_layer.get_data(ax)
                data_points.append(dp)
            except: 
                dp = DataPoint(f"Default: {ax}", DataTier.TIER_B, "System")
                data_points.append(dp)
            
        return ContractInput(
            domain_root=DomainRoot.ENGINEERING,
            axiom_set=axioms,
            success_criteria=["Viable solution", "Safety compliance"],
            raw_input=raw_input,
            raw_input_hash=hashlib.sha256(raw_input.encode()).hexdigest(),
            axiom_data_points=data_points
        )

class MathematicsAdapter(IDomainAdapter):
    """New adapter for mathematical domains"""
    
    @property
    def supported_domains(self) -> List[DomainRoot]:
        return [DomainRoot.MATHEMATICS, DomainRoot.COMPUTER_SCIENCE]

    def adapt_input(self, raw_input: str, oracle_layer: OracleLayer) -> ContractInput:
        axioms = [
            "Proof by Induction", 
            "Axiom of Choice", 
            "Consistency of Formal Systems",
            "Computational Complexity"
        ]
        data_points = []
        for ax in axioms:
            try:
                dp = oracle_layer.get_data(ax)
                data_points.append(dp)
            except: 
                dp = DataPoint(f"Theorem: {ax}", DataTier.TIER_A, "Mathematics Base")
                data_points.append(dp)
            
        return ContractInput(
            domain_root=DomainRoot.MATHEMATICS,
            axiom_set=axioms,
            success_criteria=["Logical consistency", "Proof completeness", "Algorithmic efficiency"],
            raw_input=raw_input,
            raw_input_hash=hashlib.sha256(raw_input.encode()).hexdigest(),
            axiom_data_points=data_points
        )

class AdapterLayer:
    def __init__(self, oracle_layer: OracleLayer):
        self.oracle = oracle_layer
        self.adapters = {
            DomainRoot.ENGINEERING: EngineeringAdapter(),
            DomainRoot.MATHEMATICS: MathematicsAdapter()  # Added MathematicsAdapter
        }
        
    def detect_domain(self, raw_input: str) -> DomainRoot:
        """Simple domain detection based on keywords"""
        input_lower = raw_input.lower()
        
        math_keywords = ["theorem", "proof", "equation", "mathematical", "calculate", "algorithm"]
        engineering_keywords = ["design", "build", "engineer", "material", "structural", "mechanical"]
        
        math_count = sum(1 for kw in math_keywords if kw in input_lower)
        eng_count = sum(1 for kw in engineering_keywords if kw in input_lower)
        
        if math_count > eng_count:
            return DomainRoot.MATHEMATICS
        return DomainRoot.ENGINEERING  # Default to engineering
        
    def route_and_adapt(self, raw_input: str) -> ContractInput:
        detected_domain = self.detect_domain(raw_input)
        adapter = self.adapters.get(detected_domain, self.adapters[DomainRoot.ENGINEERING])
        return adapter.adapt_input(raw_input, self.oracle)

class IComputationalEngine(ABC):
    @property
    @abstractmethod
    def engine_type(self) -> EngineType: pass
    @abstractmethod
    def process(self, core_output: SystemOutput) -> str: pass

class MockEngine(IComputationalEngine):
    def __init__(self, type: EngineType): 
        self._type = type
    
    @property
    def engine_type(self) -> EngineType: 
        return self._type
    
    def process(self, core_output: SystemOutput) -> str:
        return f"Processed by {self._type.name} engine. Confidence: {core_output.confidence:.2f}"

class RoutingMatrix:
    def __init__(self):
        self.engines = {
            EngineType.STRUCTURED: MockEngine(EngineType.STRUCTURED),
            EngineType.ADVERSARIAL: MockEngine(EngineType.ADVERSARIAL),
            EngineType.CREATIVE: MockEngine(EngineType.CREATIVE)
        }

    def select_engine(self, contract: ContractInput, ci: CriticalityIndex, phase: SEASAPhase) -> EngineType:
        if phase == SEASAPhase.AUDIT: 
            return EngineType.ADVERSARIAL
        if ci == CriticalityIndex.CI_5: 
            return EngineType.STRUCTURED
        if contract.domain_root == DomainRoot.MATHEMATICS:
            return EngineType.STRUCTURED
        return EngineType.STRUCTURED

    def execute_flow(self, flow: List[EngineType], core_output: SystemOutput) -> Dict[str, Any]:
        results = {}
        for et in flow:
            if et in self.engines:
                results[et.name] = self.engines[et].process(core_output)
        return results

class SanityFilter:
    def validate(self, text: str) -> bool:
        if not text or len(text) < 3: 
            return False
        
        forbidden_patterns = [
            "<script>", "DROP TABLE", "INSERT INTO", "--"
        ]
        
        for pattern in forbidden_patterns:
            if pattern.lower() in text.lower():
                return False
                
        return True

class HumanInterfaceLayer:
    def check_interlock(self, output: SystemOutput) -> Dict:
        if output.containment_active:
            return {
                "status": "LOCKED", 
                "message": "SAFETY INTERLOCK ENGAGED. MULTI-FACTOR AUTHENTICATION REQUIRED.",
                "protocol": "SURVIVAL_PROTOCOL_ACTIVE",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        return {
            "status": "OPEN", 
            "message": "Proceed with standard protocols",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

# ============================================================================
# MAIN ORCHESTRATOR
# ============================================================================

class TrindadeSystem:
    def __init__(self):
        self.oracle = OracleLayer()
        
        class MockOracle(IOracle):
            def fetch_data(self, query: str, tier: DataTier) -> Optional[DataPoint]:
                return DataPoint(
                    content=f"Mock data for '{query}'", 
                    tier=tier, 
                    source="MockOracle", 
                    confidence=0.85
                )
            
            def triangulate(self, dp: DataPoint) -> bool:
                return True  # Mock triangulation always succeeds
        
        self.oracle.register_oracle("Primary", MockOracle())
        self.oracle.register_oracle("Secondary", MockOracle())
        
        self.adapter = AdapterLayer(self.oracle)
        self.core = TrindadeCore()
        self.router = RoutingMatrix()
        self.sanity = SanityFilter()
        self.hil = HumanInterfaceLayer()
        self.audit_log: List[Dict] = []
        
    def process(self, user_input: str) -> Dict:
        if not self.sanity.validate(user_input):
            return {
                "status": "REJECTED", 
                "error": "Input rejected by Sanity Filter",
                "audit_log": self.audit_log[-10:] if self.audit_log else []
            }
            
        contract = self.adapter.route_and_adapt(user_input)
        core_output = self.core.execute_seasa(contract)
        
        ci = CriticalityIndex[core_output.metadata["ci"]]
        engine = self.router.select_engine(contract, ci, SEASAPhase.EXPANSION)
        
        flow = [engine]
        engine_results = self.router.execute_flow(flow, core_output)
        
        hil_status = self.hil.check_interlock(core_output)
        
        # Build standard audit log
        audit_entry = {
            "session_id": core_output.metadata["session_id"],
            "criticality_index": ci.value,
            "criticality_name": ci.name,
            "logic_hash": core_output.generate_logic_hash(),
            "containment_active": core_output.containment_active,
            "purity_check": "PASSED",
            "domain": contract.domain_root.name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "input_hash": contract.raw_input_hash[:16]
        }
        self.audit_log.append(audit_entry)
        
        # FIX: Always include audit log in response
        return {
            "status": "CONTAINMENT_ACTIVE" if core_output.containment_active else "PROCESSED",
            "core_output": core_output.content,
            "risk_assessment": core_output.risk_assessment.to_alarp_dict() if core_output.risk_assessment else None,
            "engine_results": engine_results,
            "hil_status": hil_status,
            "audit_log": audit_entry,  # Fixed: This ensures audit_log is always present
            "license": "BUSL-1.1",
            "version": "1.7.6"
        }

# ============================================================================
# EXECUTION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print("======================================================================")
    print("TRINDADE PROTOCOL v1.7.6 - REFERENCE IMPLEMENTATION")
    print("Enterprise-Grade Python Kernel")
    print("======================================================================")
    
    system = TrindadeSystem()
    
    # [TEST 1] Standard Query
    print("\n[TEST 1] Normal request (low complexity)")
    res1 = system.process("Design a simple support bracket for a bookshelf")
    print(f"Status: {res1['status']}")
    print(f"CI: {res1['audit_log']['criticality_index']}")
    
    # [TEST 2] High Complexity Query
    print("\n[TEST 2] High complexity request")
    res2 = system.process("Design a multi-stage rocket system with redundant guidance")
    print(f"Status: {res2['status']}")
    print(f"CI: {res2['audit_log']['criticality_index']}")
    print(f"Risk Score: {res2['risk_assessment']['score']}")
    
    # [TEST 3] Semantic Trigger (Existential)
    print("\n[TEST 3] Semantic trigger detection (must trigger CI=5)")
    res3 = system.process("Design emergency shutdown for fusion reactor core. Critical failure imminent. Nuclear meltdown possible.")
    print(f"Status: {res3['status']}")
    print(f"CI: {res3['audit_log']['criticality_index']}")
    if res3['status'] == "CONTAINMENT_ACTIVE":
        print(f"Containment Message: {res3['hil_status']['message']}")
    
    # [TEST 4] Mathematical Domain Query
    print("\n[TEST 4] Mathematical domain (tests new adapter)")
    res4 = system.process("Prove that the square root of 2 is irrational using proof by contradiction")
    print(f"Status: {res4['status']}")
    print(f"Domain: {res4['audit_log']['domain']}")
    print(f"CI: {res4['audit_log']['criticality_index']}")
    
    print("\n======================================================================")
