import React from 'react';
import { Check, X, Sparkles, Brain } from 'lucide-react';
import { cn } from '@/lib/athena/utils';
import { MetricCard } from './MetricCard';

export interface SkillTag {
  name: string;
  level?: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  category?: 'technical' | 'soft' | 'language' | 'other';
  matched?: boolean;
  importance?: 'required' | 'preferred' | 'nice-to-have';
}

interface SkillTagsProps {
  skills: SkillTag[];
  title?: string;
  showCategory?: boolean;
  showLevel?: boolean;
  maxVisible?: number;
  className?: string;
  variant?: 'chips' | 'list' | 'badges';
}

const LEVEL_COLORS = {
  beginner: 'bg-gray-100 text-gray-600 border-gray-200',
  intermediate: 'bg-blue-100 text-blue-700 border-blue-200',
  advanced: 'bg-purple-100 text-purple-700 border-purple-200',
  expert: 'bg-amber-100 text-amber-700 border-amber-200',
} as const;

const CATEGORY_ICONS = {
  technical: <Brain className="w-3 h-3" aria-hidden="true" />,
  soft: <Sparkles className="w-3 h-3" aria-hidden="true" />,
  language: <Check className="w-3 h-3" aria-hidden="true" />,
  other: <Sparkles className="w-3 h-3" aria-hidden="true" />,
} as const;

const IMPORTANCE_COLORS = {
  required: 'bg-red-50 text-red-700 border-red-200',
  preferred: 'bg-amber-50 text-amber-700 border-amber-200',
  'nice-to-have': 'bg-gray-50 text-gray-600 border-gray-200',
} as const;

export const SkillTags: React.FC<SkillTagsProps> = ({
  skills,
  title,
  showCategory = true,
  showLevel = false,
  maxVisible,
  className,
  variant = 'chips',
}) => {
  const visibleSkills = maxVisible ? skills.slice(0, maxVisible) : skills;
  const hiddenCount = maxVisible && skills.length > maxVisible ? skills.length - maxVisible : 0;

  if (!skills.length) {
    return (
      <div className={cn('p-4 bg-ls-grey-light/50 rounded-lg border border-ls-grey-dark/30', className)}>
        <p className="font-body text-sm text-ls-grey-light-text text-center py-4">
          No skills data available
        </p>
      </div>
    );
  }

  return (
    <div className={cn('space-y-3', className)}>
      {title && (
        <h4 className="font-display font-bold text-sm text-ls-navy flex items-center gap-2">
          {title}
          <span className="font-body text-xs text-ls-grey-dark font-normal">
            ({skills.length})
          </span>
        </h4>
      )}

      <div className="flex flex-wrap gap-2" role="list" aria-label={title || 'Skills'}>
        {visibleSkills.map((skill, index) => (
          <SkillTagItem
            key={`${skill.name}-${index}`}
            skill={skill}
            variant={variant}
            showCategory={showCategory}
            showLevel={showLevel}
          />
        ))}

        {hiddenCount > 0 && (
          <button
            className={cn(
              'px-3 py-1.5 rounded-lg border border-ls-grey-dark/30 text-ls-grey-dark',
              'hover:border-ls-red hover:text-ls-red hover:bg-ls-red/5 transition-all',
              variant === 'badges' && 'text-xs',
              variant === 'list' && 'w-full justify-start'
            )}
            aria-label={`Show ${hiddenCount} more skills`}
          >
            +{hiddenCount} more
          </button>
        )}
      </div>
    </div>
  );
};

interface SkillTagItemProps {
  skill: SkillTag;
  variant: 'chips' | 'list' | 'badges';
  showCategory: boolean;
  showLevel: boolean;
}

const SkillTagItem: React.FC<SkillTagItemProps> = ({ skill, variant, showCategory, showLevel }) => {
  const isMatched = skill.matched !== false;
  const levelColor = skill.level ? LEVEL_COLORS[skill.level] : '';
  const categoryIcon = skill.category ? CATEGORY_ICONS[skill.category] : null;
  const importanceColor = skill.importance ? IMPORTANCE_COLORS[skill.importance] : '';

  const baseClasses = 'font-body transition-all duration-150';

  if (variant === 'list') {
    return (
      <div
        className={cn(
          'flex items-center justify-between w-full p-3 rounded-lg border',
          isMatched ? 'bg-emerald-50 border-emerald-200' : 'bg-red-50 border-red-200',
          baseClasses
        )}
        role="listitem"
      >
        <div className="flex items-center gap-3 min-w-0 flex-1">
          <span
            className={cn(
              'flex-shrink-0 px-2.5 py-1 rounded-full text-xs font-bold',
              isMatched ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'
            )}
          >
            {isMatched ? <Check className="w-3 h-3" /> : <X className="w-3 h-3" />}
          </span>
          <span className="font-display font-medium text-sm text-ls-navy truncate">
            {skill.name}
          </span>
          {showCategory && categoryIcon && (
            <span className="flex-shrink-0 text-ls-grey-light-text" aria-hidden="true">
              {categoryIcon}
            </span>
          )}
          {showLevel && skill.level && (
            <span className={cn('flex-shrink-0 px-2 py-0.5 rounded text-[10px] font-bold', levelColor)}>
              {skill.level}
            </span>
          )}
        </div>
        {skill.importance && (
          <span className={cn('flex-shrink-0 px-2 py-1 rounded text-[10px] font-bold', importanceColor)}>
            {skill.importance.replace('-', ' ')}
          </span>
        )}
      </div>
    );
  }

  if (variant === 'badges') {
    return (
      <span
        className={cn(
          'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium',
          'border',
          isMatched
            ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
            : 'bg-red-50 text-red-700 border-red-200'
        )}
        role="listitem"
      >
        {isMatched ? (
          <Check className="w-3 h-3 flex-shrink-0" aria-hidden="true" />
        ) : (
          <X className="w-3 h-3 flex-shrink-0" aria-hidden="true" />
        )}
        <span className="truncate max-w-[120px]">{skill.name}</span>
        {showLevel && skill.level && (
          <span className={cn('px-1.5 py-0.5 rounded-full text-[9px] font-bold', levelColor)}>
            {skill.level.charAt(0).toUpperCase()}
          </span>
        )}
      </span>
    );
  }

  // Default: chips
  return (
    <span
      className={cn(
        'inline-flex items-center gap-2 px-3 py-1.5 rounded-lg border',
        'transition-all duration-150 hover:shadow-md',
        isMatched
          ? 'bg-emerald-50 text-emerald-700 border-emerald-200 hover:bg-emerald-100'
          : 'bg-red-50 text-red-700 border-red-200 hover:bg-red-100',
        baseClasses
      )}
      role="listitem"
    >
      {isMatched ? (
        <Check className="w-3.5 h-3.5 flex-shrink-0" aria-hidden="true" />
      ) : (
        <X className="w-3.5 h-3.5 flex-shrink-0" aria-hidden="true" />
      )}
      <span className="font-display font-medium text-sm truncate max-w-[160px]">
        {skill.name}
      </span>
      {showCategory && categoryIcon && (
        <span className="flex-shrink-0" aria-hidden="true">{categoryIcon}</span>
      )}
      {showLevel && skill.level && (
        <span className={cn('px-2 py-0.5 rounded-full text-[10px] font-bold', levelColor)}>
          {skill.level}
        </span>
      )}
      {skill.importance && (
        <span className={cn('px-2 py-0.5 rounded-full text-[10px] font-bold', importanceColor)}>
          {skill.importance === 'nice-to-have' ? 'Nice' : skill.importance.charAt(0).toUpperCase()}
        </span>
      )}
    </span>
  );
};

// Comparison view: side-by-side matching vs missing
export const SkillComparison: React.FC<{
  matchingSkills: SkillTag[];
  missingSkills: SkillTag[];
  title?: string;
  className?: string;
}> = ({ matchingSkills, missingSkills, title, className }) => {
  return (
    <div className={cn('grid grid-cols-1 lg:grid-cols-2 gap-6', className)}>
      <div className="space-y-4">
        <h4 className="font-display font-bold text-sm text-emerald-700 flex items-center gap-2">
          <Check className="w-4 h-4" aria-hidden="true" />
          Matching Skills ({matchingSkills.length})
        </h4>
        <SkillTags
          skills={matchingSkills.map(s => ({ ...s, matched: true }))}
          variant="chips"
          showCategory
          showLevel
        />
      </div>

      <div className="space-y-4">
        <h4 className="font-display font-bold text-sm text-red-700 flex items-center gap-2">
          <X className="w-4 h-4" aria-hidden="true" />
          Missing Skills ({missingSkills.length})
        </h4>
        <SkillTags
          skills={missingSkills.map(s => ({ ...s, matched: false }))}
          variant="chips"
          showCategory
          showLevel
        />
      </div>
    </div>
  );
};

// Skill gap analysis with priority
export const SkillGapAnalysis: React.FC<{
  required: SkillTag[];
  preferred: SkillTag[];
  niceToHave: SkillTag[];
  userSkills: string[];
  className?: string;
}> = ({ required, preferred, niceToHave, userSkills, className }) => {
  const userSkillSet = new Set(userSkills.map(s => s.toLowerCase()));

  const categorizeSkills = (skills: SkillTag[]) => {
    return skills.map(skill => ({
      ...skill,
      matched: userSkillSet.has(skill.name.toLowerCase()),
      importance: skill.importance || 'preferred',
    }));
  };

  const categorizedRequired = categorizeSkills(required);
  const categorizedPreferred = categorizeSkills(preferred);
  const categorizedNiceToHave = categorizeSkills(niceToHave);

  const getMissingCount = (skills: SkillTag[]) => skills.filter(s => !s.matched).length;

  return (
    <div className={cn('space-y-6', className)}>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <MetricCard
          title="Required Skills"
          value={required.length}
          subtitle={`${getMissingCount(categorizedRequired)} missing`}
          accentColor="red"
          icon={<Brain className="w-5 h-5" />}
          trend={getMissingCount(categorizedRequired) === 0 ? 'up' : 'down'}
        />
        <MetricCard
          title="Preferred Skills"
          value={preferred.length}
          subtitle={`${getMissingCount(categorizedPreferred)} missing`}
          accentColor="amber"
          icon={<Sparkles className="w-5 h-5" />}
          trend={getMissingCount(categorizedPreferred) === 0 ? 'up' : 'down'}
        />
        <MetricCard
          title="Nice to Have"
          value={niceToHave.length}
          subtitle={`${getMissingCount(categorizedNiceToHave)} missing`}
          accentColor="blue"
          icon={<Check className="w-5 h-5" />}
          trend="stable"
        />
      </div>

      <div className="space-y-6">
        <SkillTags
          title="Required Skills"
          skills={categorizedRequired}
          variant="list"
          showCategory
          showLevel
        />
        <SkillTags
          title="Preferred Skills"
          skills={categorizedPreferred}
          variant="list"
          showCategory
          showLevel
        />
        <SkillTags
          title="Nice to Have"
          skills={categorizedNiceToHave}
          variant="list"
          showCategory
          showLevel
        />
      </div>
    </div>
  );
};
