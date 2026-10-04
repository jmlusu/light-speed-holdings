import React from 'react';
import '../../brand/tokens/brand-tokens.css';

interface Leader {
  id: string;
  name: string;
  title: string;
  agentCounterpart: string;
  photo?: string;
  avatarInitials?: string;
}

const leaders: Leader[] = [
  {
    id: 'ceo',
    name: 'Jack Mlusu',
    title: 'CEO',
    agentCounterpart: 'human-ceo',
    avatarInitials: 'JM',
  },
  {
    id: 'caio',
    name: 'Chief AI Officer',
    title: 'CAIO',
    agentCounterpart: 'llm-platform-owner',
    avatarInitials: 'CA',
  },
  {
    id: 'cto',
    name: 'Chief Technology Officer',
    title: 'CTO',
    agentCounterpart: 'orchestration-owner',
    avatarInitials: 'CT',
  },
  {
    id: 'ciso',
    name: 'Chief Information Security Officer',
    title: 'CISO',
    agentCounterpart: 'security-compliance-lead',
    avatarInitials: 'CI',
  },
  {
    id: 'creative',
    name: 'Creative Director',
    title: 'Creative Director',
    agentCounterpart: 'creative-director',
    avatarInitials: 'CD',
  },
];

interface LeaderCardProps {
  leader: Leader;
}

const LeaderCard: React.FC<LeaderCardProps> = ({ leader }) => (
  <article
    className="ls-leader-card"
    style={{
      backgroundColor: 'var(--color-white, #FFFFFF)',
      border: '1px solid var(--color-navy, #070A40)',
      borderRadius: 'var(--radius-medium, 8px)',
      padding: 'var(--spacing-24, 24px)',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      textAlign: 'center',
      minWidth: '280px',
      maxWidth: '280px',
      height: '320px',
      flexShrink: 0,
    } as React.CSSProperties}
  >
    <div
      className="ls-leader-card__avatar"
      style={{
        width: '120px',
        height: '120px',
        borderRadius: '50%',
        backgroundColor: 'var(--color-navy, #070A40)',
        border: '2px solid var(--color-navy, #070A40)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: 'var(--spacing-16, 16px)',
        overflow: 'hidden',
        flexShrink: 0,
      } as React.CSSProperties}
    >
      {leader.photo ? (
        <img
          src={leader.photo}
          alt={`${leader.name} photo`}
          style={{ width: '100%', height: '100%', objectFit: 'cover' } as React.CSSProperties}
          loading="lazy"
        />
      ) : (
        <span
          style={{
            fontFamily: 'var(--font-display, Arial)',
            fontWeight: 700,
            fontSize: 'var(--size-title-xl, 32pt)',
            color: 'var(--color-white, #FFFFFF)',
          } as React.CSSProperties}
        >
          {leader.avatarInitials}
        </span>
      )}
    </div>
    <h3
      className="ls-leader-card__name"
      style={{
        fontFamily: 'var(--font-display, Arial)',
        fontWeight: 700,
        fontSize: 'var(--size-title-sm, 18pt)',
        lineHeight: 1.2,
        color: 'var(--color-navy, #070A40)',
        margin: '0 0 var(--spacing-4, 4px)',
      } as React.CSSProperties}
    >
      {leader.name}
    </h3>
    <p
      className="ls-leader-card__title"
      style={{
        fontFamily: 'var(--font-body, Arial)',
        fontWeight: 400,
        fontSize: 'var(--size-body, 14pt)',
        lineHeight: 1.4,
        color: 'var(--color-grey-dark, #6B7280)',
        margin: '0 0 var(--spacing-16, 16px)',
      } as React.CSSProperties}
    >
      {leader.title}
    </p>
    <div
      className="ls-leader-card__badges"
      style={{
        display: 'flex',
        flexDirection: 'column',
        gap: 'var(--spacing-8, 8px)',
        width: '100%',
      } as React.CSSProperties}
    >
      <span
        className="ls-leader-card__badge ls-leader-card__badge--human"
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: 'var(--font-display, Arial)',
          fontWeight: 700,
          fontSize: 'var(--size-caption, 12pt)',
          color: 'var(--color-white, #FFFFFF)',
          backgroundColor: 'var(--color-red, #E63946)',
          padding: 'var(--spacing-6, 6px) var(--spacing-12, 12px)',
          borderRadius: 'var(--radius-small, 4px)',
        } as React.CSSProperties}
      >
        Human Lead
      </span>
      <span
        className="ls-leader-card__badge ls-leader-card__badge--agent"
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: 'var(--font-display, Arial)',
          fontWeight: 700,
          fontSize: 'var(--size-caption, 12pt)',
          color: 'var(--color-navy, #070A40)',
          backgroundColor: 'var(--color-cyan, #00BFFF)',
          padding: 'var(--spacing-6, 6px) var(--spacing-12, 12px)',
          borderRadius: 'var(--radius-small, 4px)',
        } as React.CSSProperties}
      >
        Agent: {leader.agentCounterpart}
      </span>
    </div>
  </article>
);

interface LeadershipStripProps {
  className?: string;
}

export const LeadershipStrip: React.FC<LeadershipStripProps> = ({ className = '' }) => {
  return (
    <section
      className={`ls-leadership-strip ${className}`}
      aria-labelledby="leadership-title"
      style={{
        padding: 'var(--spacing-96, 96px) var(--spacing-48, 48px)',
        backgroundColor: 'var(--color-grey-light, #F2F2F2)',
      } as React.CSSProperties}
    >
      <div style={{ maxWidth: 'var(--layout-web-max-width, 1200px)', margin: '0 auto' } as React.CSSProperties}>
        <header className="ls-leadership-strip__header" style={{ marginBottom: 'var(--spacing-48, 48px)', textAlign: 'center' } as React.CSSProperties}>
          <h2
            id="leadership-title"
            className="ls-leadership-strip__title"
            style={{
              fontFamily: 'var(--font-display, Arial)',
              fontWeight: 700,
              fontSize: 'var(--size-title-xl, 32pt)',
              lineHeight: 1.2,
              color: 'var(--color-navy, #070A40)',
              margin: '0 0 var(--spacing-16, 16px)',
            } as React.CSSProperties}
          >
            The Humans Behind the Agents
          </h2>
          <p
            className="ls-leadership-strip__subtitle"
            style={{
              fontFamily: 'var(--font-body, Arial)',
              fontWeight: 400,
              fontSize: 'var(--size-body-lg, 16pt)',
              lineHeight: 1.6,
              color: 'var(--color-grey-dark, #6B7280)',
              margin: 0,
              maxWidth: '600px',
              marginLeft: 'auto',
              marginRight: 'auto',
            } as React.CSSProperties}
          >
            A hybrid human-AI leadership team: each executive has an agent counterpart
          </p>
        </header>

        <div
          className="ls-leadership-strip__scroll"
          role="list"
          style={{
            display: 'flex',
            gap: 'var(--spacing-24, 24px)',
            overflowX: 'auto',
            paddingBottom: 'var(--spacing-16, 16px)',
            scrollSnapType: 'x mandatory',
            WebkitOverflowScrolling: 'touch',
            msOverflowStyle: 'none',
            scrollbarWidth: 'none',
          } as React.CSSProperties}
        >
          {leaders.map((leader) => (
            <LeaderCard key={leader.id} leader={leader} />
          ))}
        </div>
      </div>
    </section>
  );
};

export default LeadershipStrip;
