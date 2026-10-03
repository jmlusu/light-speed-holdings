/* Leadership registry — MASTER_SPEC §15.
 * Canonical source: MISSION_AND_VISION (v2.0, Sep 2026).
 * Consumed by AboutSection. One human CEO oversees the 90-agent operation. */

export interface Leader {
  id: string;
  name: string;
  initials: string;
  title: string;
  bio: string;
}

export const leadership: readonly Leader[] = [
  {
    id: 'jack-mlusu',
    name: 'Jack Mlusu',
    initials: 'JM',
    title: 'Founder & Chief Executive Officer',
    bio: 'Founder of LightSpeed Holdings Limited and architect of the Pharos Policy Track. Leading human-in-the-loop executive authority overseeing sovereign digital transformation, SADC policy submissions, and agentic AI deployments across Africa.',
  },
];

export const founder: Leader = leadership[0];
