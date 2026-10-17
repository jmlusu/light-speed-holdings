/**
 * LightSpeed Task Queue Schema — Cloudflare Queues
 * TypeScript definitions for task messages
 * 
 * Used by: Control Plane Workers, Queue Consumers, Dashboard API
 * Version: 1.0
 * Date: October 3, 2026
 */

// ─────────────────────────────────────────────────────────────────
// Core Types
// ─────────────────────────────────────────────────────────────────

/** Agent type classification from registry */
export type AgentType = "executive" | "specialist" | "board";

/** Task priority levels */
export type TaskPriority = "low" | "medium" | "high" | "critical";

/** Task status lifecycle */
export type TaskStatus = 
  | "queued"           // In queue, waiting for consumer
  | "claimed"          // Consumer claimed, not yet running
  | "running"          // Actively executing
  | "checkpointing"    // Serializing state to Durable Object
  | "completed"        // Finished successfully
  | "failed"           // Error during execution
  | "timeout"          // Exceeded timeout_seconds
  | "escalated"        // Max retries exceeded, human review needed
  | "dead_letter";     // Moved to DLQ, awaiting manual intervention

/** Human approval tier (from tier_rules.py — 5 tiers) */
export type ApprovalTier = 1 | 2 | 3 | 4 | 5;

/** Source of task creation */
export type TaskSource = "scheduler" | "manual" | "delegation" | "webhook";

/** Canonical tool vocabulary (OpenCode v2 permission keys) */
export type CanonicalTool = 
  | "read" 
  | "edit" 
  | "grep" 
  | "list" 
  | "bash" 
  | "webfetch" 
  | "task";

/** Legacy tool aliases (accepted but not emitted in new cards) */
export type LegacyTool = 
  | "write" 
  | "execute" 
  | "delegate" 
  | "web_search" 
  | "websearch" 
  | "code_interpreter";

// ─────────────────────────────────────────────────────────────────
// Task Input / Output
// ─────────────────────────────────────────────────────────────────

export interface TaskInput {
  /** Primary instruction for the agent */
  instruction: string;
  
  /** Optional additional context */
  context?: string;
  
  /** Paths to artifact files in R2 storage */
  files?: string[];
  
  /** Parent task IDs this task depends on */
  dependencies?: string[];
  
  /** Additional metadata for the agent */
  metadata?: Record<string, unknown>;
}

export interface TaskResult {
  /** Agent's final output text */
  output: string;
  
  /** Artifact file paths in R2 */
  artifacts: string[];
  
  /** Token usage statistics */
  tokens_used: {
    prompt: number;
    completion: number;
    total: number;
  };
  
  /** Cost in USD */
  cost_usd: number;
  
  /** Model actually used (after routing/fallback) */
  model_used: string;
  
  /** Execution duration in milliseconds */
  duration_ms: number;
  
  /** Tools invoked during execution */
  tools_invoked: CanonicalTool[];
  
  /** Iterations completed (for AgentLoop) */
  iterations: number;
  
  /** Additional result metadata */
  metadata?: Record<string, unknown>;
}

export interface TaskError {
  /** Error message */
  message: string;
  
  /** Error code for categorization */
  code: string;
  
  /** Stack trace if available */
  stack?: string;
  
  /** Whether error is retryable */
  retryable: boolean;
  
  /** Additional error context */
  context?: Record<string, unknown>;
}

// ─────────────────────────────────────────────────────────────────
// Main Task Interface
// ─────────────────────────────────────────────────────────────────

export interface LightSpeedTask {
  // ── Identity ──
  /** UUID v7 (time-ordered) — globally unique */
  task_id: string;
  
  /** Registry ID of target agent (e.g., "chief_of_staff") */
  agent_id: string;
  
  /** Agent classification */
  agent_type: AgentType;
  
  /** Task category for routing */
  task_type: string;
  
  // ── Priority & Scheduling ──
  priority: TaskPriority;
  
  /** ISO 8601 timestamp when task was created */
  created_at: string;
  
  /** Optional ISO 8601 timestamp for delayed execution */
  scheduled_at?: string;
  
  // ── Status & Retry ──
  status: TaskStatus;
  
  /** Current attempt number (0-indexed) */
  attempt: number;
  
  /** Maximum retry attempts (default 3 from ADR-015) */
  max_attempts: number;
  
  /** Timeout in seconds (default 1800 = 30 min) */
  timeout_seconds: number;
  
  // ── Input / Output ──
  input: TaskInput;
  
  /** Populated on completion */
  result?: TaskResult;
  
  /** Populated on failure */
  error?: TaskError;
  
  // ── Model Routing ──
  /** Required tool capabilities */
  required_capabilities: CanonicalTool[];
  
  /** Preferred model (optional — router will select if omitted) */
  preferred_model?: string;
  
  /** Ordered fallback model chain */
  fallback_models?: string[];
  
  // ── Human Approval ──
  /** Whether this task requires human approval before execution */
  requires_human_approval: boolean;
  
  /** Approval tier (1-5) if approval required */
  approval_tier?: ApprovalTier;
  
  /** Approval request ID if pending */
  approval_request_id?: string;
  
  // ── Delegation & Tracing ──
  /** Parent task ID for delegation tracking */
  parent_task?: string;
  
  /** Correlation ID for distributed tracing */
  correlation_id: string;
  
  // ── Metadata ──
  /** Source of task creation */
  source: TaskSource;
  
  /** Tags for filtering/querying */
  tags: string[];
  
  /** Additional custom metadata */
  metadata?: Record<string, unknown>;
  
  // ── Timestamps (populated by system) ──
  /** When task was claimed by consumer */
  claimed_at?: string;
  
  /** When execution started */
  started_at?: string;
  
  /** When task reached terminal state */
  completed_at?: string;
  
  /** Lease expiration for claimed tasks */
  lease_expires_at?: string;
  
  /** Consumer worker ID that claimed this task */
  claimed_by?: string;
}

// ─────────────────────────────────────────────────────────────────
// Queue Message Envelope
// ─────────────────────────────────────────────────────────────────

/** Wrapper for Cloudflare Queues message */
export interface QueueMessage<T = LightSpeedTask> {
  /** Queue message ID */
  id: string;
  
  /** Message body */
  body: T;
  
  /** Timestamp when message was enqueued */
  timestamp: string;
  
  /** Number of delivery attempts */
  attempts: number;
  
  /** Message metadata */
  metadata?: Record<string, unknown>;
}

// ─────────────────────────────────────────────────────────────────
// Consumer Worker Types
// ─────────────────────────────────────────────────────────────────

export interface ConsumerConfig {
  /** Consumer worker identifier */
  worker_id: string;
  
  /** Agent types this consumer handles */
  agent_types: AgentType[];
  
  /** Maximum concurrent tasks */
  max_concurrency: number;
  
  /** Lease duration in seconds */
  lease_seconds: number;
  
  /** Heartbeat interval in seconds */
  heartbeat_interval_seconds: number;
  
  /** Queue names to consume from */
  queue_names: string[];
  
  /** Dead letter queue name */
  dlq_name: string;
}

export interface TaskClaimResult {
  /** Whether claim was successful */
  success: boolean;
  
  /** The claimed task (if successful) */
  task?: LightSpeedTask;
  
  /** Error message if claim failed */
  error?: string;
  
  /** Lease expiration timestamp */
  lease_expires_at?: string;
}

export interface HeartbeatResult {
  /** Whether heartbeat was accepted */
  success: boolean;
  
  /** Updated lease expiration */
  lease_expires_at?: string;
  
  /** Error if heartbeat failed */
  error?: string;
}

export interface CheckpointPayload {
  /** Agent's serialized state */
  agent_state: unknown;
  
  /** Current iteration */
  iteration: number;
  
  /** Tools used so far */
  tools_used: CanonicalTool[];
  
  /** Token usage so far */
  tokens_used: {
    prompt: number;
    completion: number;
    total: number;
  };
  
  /** Cost so far */
  cost_usd: number;
  
  /** Timestamp */
  timestamp: string;
}

// ─────────────────────────────────────────────────────────────────
// Scheduler Types
// ─────────────────────────────────────────────────────────────────

export interface ScheduledTask {
  /** Task template to instantiate */
  task_template: Omit<LightSpeedTask, "task_id" | "created_at" | "status" | "attempt" | "correlation_id">;
  
  /** Cron expression (UTC) */
  cron: string;
  
  /** Timezone for cron (IANA) */
  timezone?: string;
  
  /** Whether schedule is active */
  enabled: boolean;
  
  /** Maximum concurrent instances of this scheduled task */
  max_concurrent: number;
  
  /** Tags for the scheduled task */
  tags: string[];
}

export interface ScheduleTrigger {
  /** Scheduled task ID */
  schedule_id: string;
  
  /** Trigger timestamp */
  triggered_at: string;
  
  /** Generated task ID */
  task_id: string;
}

// ─────────────────────────────────────────────────────────────────
// Dead Letter Queue Types
// ─────────────────────────────────────────────────────────────────

export interface DeadLetterEntry {
  /** Original task */
  task: LightSpeedTask;
  
  /** Reason for DLQ placement */
  reason: "max_retries_exceeded" | "timeout" | "consumer_failed" | "lease_expired" | "validation_failed";
  
  /** Error details */
  error: TaskError;
  
  /** Timestamp when moved to DLQ */
  dlq_timestamp: string;
  
  /** Number of retry attempts made */
  retry_count: number;
  
  /** Consumer that failed */
  failed_consumer?: string;
  
  /** Whether human has reviewed */
  reviewed: boolean;
  
  /** Review notes */
  review_notes?: string;
}

// ─────────────────────────────────────────────────────────────────
// API Types (Dashboard / Control Plane)
// ─────────────────────────────────────────────────────────────────

export interface TaskQueryParams {
  /** Filter by agent ID */
  agent_id?: string;
  
  /** Filter by agent type */
  agent_type?: AgentType;
  
  /** Filter by status */
  status?: TaskStatus | TaskStatus[];
  
  /** Filter by priority */
  priority?: TaskPriority;
  
  /** Filter by task type */
  task_type?: string;
  
  /** Filter by date range (ISO 8601) */
  created_after?: string;
  created_before?: string;
  
  /** Filter by correlation ID */
  correlation_id?: string;
  
  /** Filter by tags */
  tags?: string[];
  
  /** Pagination */
  limit?: number;
  offset?: number;
  
  /** Sort order */
  sort_by?: "created_at" | "priority" | "status" | "agent_id";
  sort_order?: "asc" | "desc";
}

export interface TaskListResponse {
  tasks: LightSpeedTask[];
  total: number;
  limit: number;
  offset: number;
}

export interface TaskStats {
  total: number;
  by_status: Record<TaskStatus, number>;
  by_agent: Record<string, number>;
  by_priority: Record<TaskPriority, number>;
  avg_duration_ms: number;
  success_rate: number;
  total_cost_usd: number;
  total_tokens: number;
}

export interface EnqueueTaskRequest {
  /** Task to enqueue (without system-generated fields) */
  task: Omit<LightSpeedTask, "task_id" | "created_at" | "status" | "attempt" | "correlation_id" | "claimed_at" | "started_at" | "completed_at" | "lease_expires_at" | "claimed_by">;
  
  /** Optional delay before enqueueing */
  delay_seconds?: number;
  
  /** Priority override */
  priority?: TaskPriority;
}

export interface EnqueueTaskResponse {
  success: boolean;
  task_id?: string;
  error?: string;
}

export interface RetryTaskRequest {
  task_id: string;
  reason?: string;
  reset_attempt?: boolean; // default false
}

export interface CancelTaskRequest {
  task_id: string;
  reason?: string;
}

// ─────────────────────────────────────────────────────────────────
// Validation Helpers
// ─────────────────────────────────────────────────────────────────

/** Required fields for task creation */
export const REQUIRED_TASK_FIELDS: (keyof LightSpeedTask)[] = [
  "agent_id",
  "agent_type",
  "task_type",
  "priority",
  "input",
  "required_capabilities",
  "requires_human_approval",
  "timeout_seconds",
  "max_attempts",
  "source",
  "tags",
];

/** Validate task has all required fields */
export function validateTask(task: Partial<LightSpeedTask>): { valid: boolean; missing: string[] } {
  const missing = REQUIRED_TASK_FIELDS.filter(field => !(field in task));
  return { valid: missing.length === 0, missing };
}

/** Generate UUID v7 (time-ordered) */
export function generateTaskId(): string {
  // In production, use a proper UUID v7 library
  // This is a placeholder
  return crypto.randomUUID();
}

/** Generate correlation ID */
export function generateCorrelationId(): string {
  return crypto.randomUUID();
}