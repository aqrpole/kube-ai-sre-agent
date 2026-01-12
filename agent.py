import time
from helpers import (
    init_k8s_clients,
    load_policy,
    collect_problematic_pods,
    collect_pod_events,
    collect_pod_logs,
    collect_pod_metrics,
    build_incident_context,
    #llm_diagnose,
    evaluate_policy,
    report_incident,
    query_ollama_llm,
    parse_llm_response
)
from kubernetes import client, config

POLL_INTERVAL_SECONDS = 15
NAMESPACE             = "demo"

def main():
    print ("🚀 kube-ai-sre-agent started (continuous, memory-only MVP)")

    # STEP 1: Load policy
    policy = load_policy ()

    # STEP 2: Initialize Kubernetes clients
    core_v1, custom_api = init_k8s_clients ()

    while True:
        print ("\n🔄 Scanning cluster state...")

        # STEP 3: Detect problematic pods (OOMKilled / CrashLoopBackOff)
        pods = collect_problematic_pods (core_v1)

        for pod, status in pods:
            print (f"⚠️  Detected problematic pod: {pod.metadata.name}")

            # STEP 4: Collect signals
            events         = collect_pod_events (core_v1, pod)
            logs           = collect_pod_logs (core_v1, pod)
            metrics        = collect_pod_metrics (custom_api, pod)

            # STEP 5: Correlate signals into incident context
            context        = build_incident_context (pod, status, events, logs, metrics)

            # STEP 6: LLM reasoning (diagnosis only)
            raw_llm_output = query_ollama_llm (context)
            diagnosis      = parse_llm_response (raw_llm_output) 

            # STEP 7: Policy evaluation (safety gate)
            decision       = evaluate_policy (policy, pod, diagnosis)

            # STEP 8: Report (no auto-remediation in MVP)
            report_incident (pod, context, diagnosis, decision)

        time.sleep (POLL_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
