import React from 'react';
import { Icon3DProps, getPixelSize, Icon3DName } from './icon3d-registry';

export const Icon3D: React.FC<Icon3DProps> = ({
  name,
  size = 'md',
  className = '',
  alt,
  isInteractive = false,
}) => {
  const px = getPixelSize(size);
  const uid = React.useId().replace(/:/g, '');
  const filterId = `f-shadow-${uid}`;
  const glassGradId = `g-glass-${uid}`;
  const glassDeepGradId = `g-glass-deep-${uid}`;
  const goldGradId = `g-gold-${uid}`;
  const goldLightGradId = `g-gold-light-${uid}`;
  const cyanGradId = `g-cyan-${uid}`;
  const silverGradId = `g-silver-${uid}`;
  const shadowGradId = `g-shadow-${uid}`;

  // Shared Defs for 3D Specular Lighting, Blue Glass & Metallic Gold
  const renderDefs = () => (
    <defs>
      {/* 3D Realistic Soft Drop Shadow */}
      <filter id={filterId} x="-25%" y="-25%" width="150%" height="150%">
        <feDropShadow dx="0" dy="7" stdDeviation="6" floodColor="#070A40" floodOpacity="0.4" />
        <feDropShadow dx="0" dy="2" stdDeviation="2.5" floodColor="#00BFFF" floodOpacity="0.25" />
      </filter>

      {/* Transparent Cyan/Blue Glass Gradient */}
      <linearGradient id={glassGradId} x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#38BDF8" stopOpacity="0.9" />
        <stop offset="25%" stopColor="#00BFFF" stopOpacity="0.8" />
        <stop offset="70%" stopColor="#070A40" stopOpacity="0.75" />
        <stop offset="100%" stopColor="#0284C7" stopOpacity="0.85" />
      </linearGradient>

      {/* Deep Blue Solid/Semi-Transparent Glass */}
      <linearGradient id={glassDeepGradId} x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#1E3A8A" stopOpacity="0.95" />
        <stop offset="50%" stopColor="#0B1A48" stopOpacity="0.9" />
        <stop offset="100%" stopColor="#070A40" stopOpacity="0.95" />
      </linearGradient>

      {/* Polished Metallic Gold Gradient */}
      <linearGradient id={goldGradId} x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#FFF7CC" />
        <stop offset="20%" stopColor="#FDE047" />
        <stop offset="45%" stopColor="#D97706" />
        <stop offset="75%" stopColor="#B45309" />
        <stop offset="90%" stopColor="#F59E0B" />
        <stop offset="100%" stopColor="#FEF08A" />
      </linearGradient>

      {/* Light Champagne Gold Accent */}
      <linearGradient id={goldLightGradId} x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stopColor="#FFFBEB" />
        <stop offset="50%" stopColor="#FDE68A" />
        <stop offset="100%" stopColor="#F59E0B" />
      </linearGradient>

      {/* Cyan Glass Rim & Refraction Gradient */}
      <linearGradient id={cyanGradId} x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stopColor="#BAE6FD" stopOpacity="0.9" />
        <stop offset="50%" stopColor="#00BFFF" stopOpacity="0.95" />
        <stop offset="100%" stopColor="#0284C7" stopOpacity="0.8" />
      </linearGradient>

      {/* Polished Metallic Silver/Chrome Gradient */}
      <linearGradient id={silverGradId} x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#FFFFFF" />
        <stop offset="35%" stopColor="#E2E8F0" />
        <stop offset="70%" stopColor="#94A3B8" />
        <stop offset="100%" stopColor="#CBD5E1" />
      </linearGradient>

      {/* Ground Contact Shadow Radial Gradient */}
      <radialGradient id={shadowGradId} cx="50%" cy="50%" r="50%">
        <stop offset="0%" stopColor="#070A40" stopOpacity="0.5" />
        <stop offset="80%" stopColor="#070A40" stopOpacity="0.15" />
        <stop offset="100%" stopColor="#070A40" stopOpacity="0" />
      </radialGradient>
    </defs>
  );

  const renderIconContent = (iconName: Icon3DName) => {
    switch (iconName) {
      // ─────────────────────────────────────────────────────────────
      // 1. PEN / EDIT (Reference: image_89d7c5fd.png row 1, col 1)
      // ─────────────────────────────────────────────────────────────
      case 'pen':
      case 'edit':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="58" rx="20" ry="3.5" fill={`url(#${shadowGradId})`} />
            <g transform="rotate(-40 32 32)">
              {/* Top Cyan Cap button */}
              <ellipse cx="32" cy="11" rx="5" ry="2.5" fill={`url(#${cyanGradId})`} />
              {/* Upper Pen Body - Glossy Blue Glass */}
              <rect x="27" y="11" width="10" height="15" rx="3" fill={`url(#${glassGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1" />
              {/* Metallic Gold Pocket Clip */}
              <path d="M 37 14 L 39 15 L 39 26 L 37 25 Z" fill={`url(#${goldGradId})`} />
              <circle cx="38" cy="27" r="1.5" fill={`url(#${goldGradId})`} />
              {/* Metallic Gold Central Trim Ring */}
              <rect x="26.5" y="26" width="11" height="4" rx="1.5" fill={`url(#${goldGradId})`} stroke="#FFF7CC" strokeWidth="0.6" />
              {/* Lower Pen Barrel - Deep Blue Glass with Specular Glint */}
              <rect x="27" y="30" width="10" height="16" rx="2" fill={`url(#${glassDeepGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="0.8" />
              <path d="M 28 30 L 29 45" stroke="#FFFFFF" strokeWidth="1" strokeOpacity="0.5" strokeLinecap="round" />
              {/* Metallic Gold Beveled Nib Section */}
              <polygon points="27,46 37,46 32,56" fill={`url(#${goldGradId})`} stroke="#FFF7CC" strokeWidth="0.8" />
              {/* Pen Tip Point */}
              <polygon points="31,54 33,54 32,57" fill="#070A40" />
            </g>
          </g>
        );

      // ─────────────────────────────────────────────────────────────
      // 2. COINS / FINANCE / REVENUE (Reference: row 1, col 2)
      // ─────────────────────────────────────────────────────────────
      case 'finance':
      case 'coins':
      case 'revenue':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="34" cy="58" rx="24" ry="4" fill={`url(#${shadowGradId})`} />
            {/* Stack of Metallic Gold Coins */}
            {[48, 43, 38, 33, 28, 23, 18].map((y, idx) => (
              <g key={idx}>
                {/* Coin edge cylinder */}
                <path d={`M 15 ${y} L 15 ${y + 4} C 15 ${y + 7} 25 ${y + 8} 35 ${y + 8} C 45 ${y + 8} 51 ${y + 7} 51 ${y + 4} L 51 ${y} Z`} fill={`url(#${goldGradId})`} />
                {/* Coin top face */}
                <ellipse cx="33" cy={y} rx="18" ry="4.5" fill={idx === 6 ? `url(#${goldLightGradId})` : `url(#${goldGradId})`} stroke="#FFF7CC" strokeWidth="0.8" />
              </g>
            ))}
            {/* Embossed dollar sign on top coin */}
            <text x="33" y="19.5" fontSize="7" fontWeight="900" fill="#B45309" textAnchor="middle" opacity="0.85">$</text>

            {/* Front Tilted Gold Coin with Big Embossed '$' */}
            <g transform="translate(4, 0)">
              <ellipse cx="44" cy="38" rx="14" ry="14" fill={`url(#${goldGradId})`} stroke="#FFF7CC" strokeWidth="1.5" />
              <ellipse cx="44" cy="38" rx="11" ry="11" fill="none" stroke="#B45309" strokeWidth="1.2" />
              <ellipse cx="43" cy="35" rx="9" ry="6" fill="#FFFFFF" opacity="0.3" />
              <text x="44" y="44" fontSize="16" fontWeight="900" fill="#B45309" textAnchor="middle" fontStyle="italic">$</text>
            </g>
          </g>
        );

      // ─────────────────────────────────────────────────────────────
      // 3. SAFE / SECURITY / VAULT (Reference: row 1, col 3)
      // ─────────────────────────────────────────────────────────────
      case 'safe':
      case 'security':
      case 'vault':
      case 'compliance':
      case 'governance':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="58" rx="22" ry="4" fill={`url(#${shadowGradId})`} />
            {/* Safe Feet */}
            <rect x="14" y="52" width="6" height="4" rx="1.5" fill={`url(#${cyanGradId})`} />
            <rect x="44" y="52" width="6" height="4" rx="1.5" fill={`url(#${cyanGradId})`} />
            {/* 3D Transparent Blue Glass Outer Safe Cube */}
            <rect x="12" y="12" width="40" height="42" rx="8" fill={`url(#${glassGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="2.5" />
            {/* Recessed Door Chamber */}
            <rect x="16" y="16" width="32" height="34" rx="5" fill={`url(#${glassDeepGradId})`} stroke={`url(#${goldGradId})`} strokeWidth="1.2" />
            {/* Specular Edge Highlights */}
            <path d="M 14 16 C 14 14 16 14 18 14 L 46 14" stroke="#FFFFFF" strokeWidth="1.5" strokeLinecap="round" opacity="0.6" />
            <path d="M 14 16 L 14 48" stroke="#FFFFFF" strokeWidth="1.2" strokeLinecap="round" opacity="0.4" />
            {/* Heavy-Duty Metallic Hinges on Right */}
            <rect x="46" y="20" width="5" height="6" rx="1.5" fill={`url(#${silverGradId})`} stroke={`url(#${goldGradId})`} strokeWidth="0.8" />
            <rect x="46" y="38" width="5" height="6" rx="1.5" fill={`url(#${silverGradId})`} stroke={`url(#${goldGradId})`} strokeWidth="0.8" />
            {/* Rotary Combination Dial - Silver & Gold */}
            <circle cx="28" cy="33" r="9" fill={`url(#${silverGradId})`} stroke={`url(#${goldGradId})`} strokeWidth="1.5" />
            <circle cx="28" cy="33" r="6" fill={`url(#${glassDeepGradId})`} />
            <circle cx="28" cy="33" r="3" fill={`url(#${goldGradId})`} />
            <line x1="28" y1="24.5" x2="28" y2="27" stroke="#FFF7CC" strokeWidth="1.2" strokeLinecap="round" />
            {/* Door Lever Handle on Right */}
            <rect x="40" y="30" width="3" height="6" rx="1" fill={`url(#${goldGradId})`} />
          </g>
        );

      // ─────────────────────────────────────────────────────────────
      // 4. FOLDER / DOCUMENTS / RECORDS (Reference: row 2, col 1)
      // ─────────────────────────────────────────────────────────────
      case 'folder':
      case 'documents':
      case 'records':
      case 'reports':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="58" rx="22" ry="4" fill={`url(#${shadowGradId})`} />
            {/* Back Folder Flap - Deep Blue Glass with Gold Tab */}
            <path d="M 10 20 C 10 17 12 15 15 15 L 24 15 L 28 19 L 51 19 C 54 19 56 21 56 24 L 56 46 L 10 46 Z" fill={`url(#${glassDeepGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1.2" />
            {/* Gold Interior Partition Tab */}
            <path d="M 14 18 C 14 16 16 15 18 15 L 25 15 L 29 18 L 48 18 C 50 18 52 19 52 21 L 52 26 L 14 26 Z" fill={`url(#${goldGradId})`} stroke="#FFF7CC" strokeWidth="0.8" />
            {/* White Document Sheets Inserted Inside */}
            <rect x="16" y="21" width="32" height="20" rx="2" fill="#FFFFFF" opacity="0.95" />
            <line x1="20" y1="25" x2="34" y2="25" stroke="#CBD5E1" strokeWidth="1.5" strokeLinecap="round" />
            <line x1="20" y1="29" x2="42" y2="29" stroke="#CBD5E1" strokeWidth="1.5" strokeLinecap="round" />
            {/* Front Transparent Cyan/Blue Glass Pocket with Beveled Edge */}
            <polygon points="8,32 56,32 53,52 11,52" fill={`url(#${glassGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="2" />
            {/* Front Glass Specular Highlight */}
            <path d="M 12 34 L 52 34 L 50 42 L 13 42 Z" fill="#FFFFFF" opacity="0.35" />
            {/* Beveled Bottom Rim */}
            <line x1="12" y1="52" x2="52" y2="52" stroke={`url(#${goldGradId})`} strokeWidth="2" strokeLinecap="round" />
          </g>
        );

      // ─────────────────────────────────────────────────────────────
      // 5. TRASH / DELETE / ARCHIVE (Reference: row 2, col 2)
      // ─────────────────────────────────────────────────────────────
      case 'trash':
      case 'delete':
      case 'archive':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="58" rx="18" ry="4" fill={`url(#${shadowGradId})`} />
            {/* Top Rim Collar - Transparent Cyan Glass Torus */}
            <ellipse cx="32" cy="18" rx="18" ry="5" fill={`url(#${cyanGradId})`} stroke="#FFFFFF" strokeWidth="1" />
            <ellipse cx="32" cy="18" rx="14" ry="3.5" fill="#070A40" opacity="0.85" />
            {/* Metallic Gold Lip Trim */}
            <ellipse cx="32" cy="18" rx="18" ry="5" fill="none" stroke={`url(#${goldGradId})`} strokeWidth="1" />
            {/* Fluted Transparent Blue Glass Bucket Body */}
            <path d="M 14 18 L 19 54 C 19 56 25 58 32 58 C 39 58 45 56 45 54 L 50 18 Z" fill={`url(#${glassGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1.5" />
            {/* Fluted Vertical Glass Ribs with Refraction */}
            {[-10, -5, 0, 5, 10].map((offset, i) => (
              <line
                key={i}
                x1={32 + offset * 1.3}
                y1="23"
                x2={32 + offset * 0.9}
                y2="53"
                stroke="#BAE6FD"
                strokeWidth="2"
                strokeOpacity="0.6"
                strokeLinecap="round"
              />
            ))}
            {/* Base Ring Accent */}
            <ellipse cx="32" cy="54" rx="13" ry="3.5" fill="none" stroke={`url(#${goldGradId})`} strokeWidth="1.2" />
          </g>
        );

      // ─────────────────────────────────────────────────────────────
      // 6. STAR / FAVORITE / VALUE / RATING (Reference: row 2, col 3)
      // ─────────────────────────────────────────────────────────────
      case 'star':
      case 'favorite':
      case 'value':
      case 'rating':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="58" rx="20" ry="4" fill={`url(#${shadowGradId})`} />
            {/* 3D Beveled Faceted Metallic Gold Star Body */}
            <polygon
              points="32,8 39,23 55,24 43,36 47,52 32,43 17,52 21,36 9,24 25,23"
              fill={`url(#${goldGradId})`}
              stroke="#FFF7CC"
              strokeWidth="1.5"
              strokeLinejoin="round"
            />
            {/* 3D Star Facet Shading */}
            <polygon points="32,8 32,43 39,23" fill="#FFE066" opacity="0.6" />
            <polygon points="32,43 47,52 43,36" fill="#B45309" opacity="0.5" />
            <polygon points="32,43 17,52 21,36" fill="#92400E" opacity="0.6" />
            <polygon points="32,8 32,43 25,23" fill="#FFFBEB" opacity="0.5" />
            <polygon points="43,36 55,24 39,23" fill="#F59E0B" opacity="0.4" />
            {/* Specular Star Center Bevel Highlight */}
            <circle cx="32" cy="30" r="3" fill="#FFFFFF" opacity="0.6" />
          </g>
        );

      // ─────────────────────────────────────────────────────────────
      // 7. CHART / ANALYTICS / STATISTICS (Reference: row 3, col 1)
      // ─────────────────────────────────────────────────────────────
      case 'chart':
      case 'analytics':
      case 'statistics':
      case 'dashboard':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="58" rx="22" ry="4" fill={`url(#${shadowGradId})`} />
            {/* 3D Transparent Glass Plaque Slab with Rounded Corners */}
            <rect x="10" y="10" width="44" height="44" rx="8" fill={`url(#${glassGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="2" />
            {/* Grid Lines Etched in Glass */}
            {[20, 28, 36, 44].map((y, idx) => (
              <line key={idx} x1="16" y1={y} x2="48" y2={y} stroke="#BAE6FD" strokeWidth="0.8" strokeOpacity="0.4" />
            ))}
            {[22, 30, 38, 46].map((x, idx) => (
              <line key={idx} x1={x} y1="16" x2={x} y2="48" stroke="#BAE6FD" strokeWidth="0.8" strokeOpacity="0.4" />
            ))}
            {/* 3 Rising 3D Blue Glass Bar Columns */}
            {/* Bar 1 (Short) */}
            <rect x="17" y="38" width="6" height="10" rx="1.5" fill={`url(#${glassDeepGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1" />
            {/* Bar 2 (Medium) */}
            <rect x="26" y="30" width="6" height="18" rx="1.5" fill={`url(#${glassDeepGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1" />
            {/* Bar 3 (Tall) */}
            <rect x="35" y="20" width="6" height="28" rx="1.5" fill={`url(#${glassDeepGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1" />
            {/* Ascending 3D Metallic Gold Trend Arrow */}
            <path d="M 16 38 L 26 28 L 34 32 L 46 16" fill="none" stroke={`url(#${goldGradId})`} strokeWidth="3.5" strokeLinecap="round" strokeLinejoin="round" />
            <polygon points="43,14 49,15 48,21" fill={`url(#${goldGradId})`} stroke="#FFF7CC" strokeWidth="0.8" />
          </g>
        );

      // ─────────────────────────────────────────────────────────────
      // 8. HOME / HOUSE / BUILDING / PROPERTY (Reference: row 3, col 2)
      // ─────────────────────────────────────────────────────────────
      case 'home':
      case 'house':
      case 'building':
      case 'property':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="58" rx="22" ry="4" fill={`url(#${shadowGradId})`} />
            {/* Chimney on Top Right */}
            <rect x="38" y="16" width="6" height="12" rx="1.5" fill={`url(#${glassDeepGradId})`} stroke={`url(#${goldGradId})`} strokeWidth="1" />
            {/* 3D Transparent Blue Glass House Body */}
            <rect x="15" y="28" width="34" height="26" rx="4" fill={`url(#${glassGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1.8" />
            {/* Deep Blue Gable Roof */}
            <polygon points="32,10 52,28 12,28" fill={`url(#${glassDeepGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1.5" />
            {/* Metallic Gold Roof Eaves / Fascia Trim */}
            <line x1="10" y1="29" x2="32" y2="9" stroke={`url(#${goldGradId})`} strokeWidth="3" strokeLinecap="round" />
            <line x1="32" y1="9" x2="54" y2="29" stroke={`url(#${goldGradId})`} strokeWidth="3" strokeLinecap="round" />
            <circle cx="32" cy="9" r="2" fill="#FFF7CC" />
            {/* Metallic Gold Trimmed Arched Doorway */}
            <path d="M 27 54 L 27 38 C 27 34 37 34 37 38 L 37 54 Z" fill="#070A40" stroke={`url(#${goldGradId})`} strokeWidth="2.5" />
            {/* Door Knocker / Handle */}
            <circle cx="35" cy="44" r="1.5" fill={`url(#${goldGradId})`} />
          </g>
        );

      // ─────────────────────────────────────────────────────────────
      // 9. NOTEPAD / NOTEBOOK / TASKS / REPORTS (Reference: row 3, col 3)
      // ─────────────────────────────────────────────────────────────
      case 'notepad':
      case 'notebook':
      case 'tasks':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="58" rx="20" ry="4" fill={`url(#${shadowGradId})`} />
            {/* 3D Blue Glass Spiral Notebook Body */}
            <rect x="14" y="14" width="36" height="42" rx="6" fill={`url(#${glassDeepGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="2" />
            {/* Top Glass Specular Bevel Highlight */}
            <path d="M 16 16 C 16 15 18 15 20 15 L 44 15 C 46 15 48 15 48 16 L 48 24 L 16 24 Z" fill="#FFFFFF" opacity="0.25" />
            {/* Metallic Silver/Gold Wire Spiral Rings */}
            {[18, 24, 30, 36, 42, 46].map((x, i) => (
              <g key={i}>
                <ellipse cx={x} cy="14" rx="2" ry="4" fill={`url(#${silverGradId})`} stroke={`url(#${goldGradId})`} strokeWidth="0.8" />
              </g>
            ))}
            {/* Horizontal Ruled Lines - White & Gold */}
            {[24, 30, 36, 42, 48].map((y, i) => (
              <line
                key={i}
                x1="20"
                y1={y}
                x2={i % 2 === 0 ? "44" : "38"}
                y2={y}
                stroke={i === 0 ? `url(#${goldGradId})` : "#FFFFFF"}
                strokeWidth={i === 0 ? "2.5" : "1.8"}
                strokeOpacity={i === 0 ? "1" : "0.75"}
                strokeLinecap="round"
              />
            ))}
          </g>
        );

      // ─────────────────────────────────────────────────────────────
      // EXTENDED ENTERPRISE AI ICONS (Matching same 3D Material Suite)
      // ─────────────────────────────────────────────────────────────
      case 'intelligence':
      case 'brain':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="58" rx="22" ry="4" fill={`url(#${shadowGradId})`} />
            {/* 3D Glass Brain Base / Crystal Structure */}
            <path
              d="M 18 20 C 14 20 10 25 11 32 C 10 38 14 44 20 45 C 24 46 28 44 32 40 C 36 44 40 46 44 45 C 50 44 54 38 53 32 C 54 25 50 20 46 20 C 41 20 37 24 32 26 C 27 24 23 20 18 20 Z"
              fill={`url(#${glassGradId})`}
              stroke={`url(#${cyanGradId})`}
              strokeWidth="2"
            />
            {/* Metallic Gold Synapse Core */}
            <path d="M 24 32 Q 32 24 40 32 Q 32 40 24 32 Z" fill={`url(#${goldGradId})`} stroke="#FFF7CC" strokeWidth="1" />
            <circle cx="20" cy="33" r="3" fill={`url(#${goldGradId})`} />
            <circle cx="32" cy="25" r="3.5" fill={`url(#${goldGradId})`} />
            <circle cx="44" cy="33" r="3" fill={`url(#${goldGradId})`} />
            <line x1="20" y1="33" x2="32" y2="25" stroke={`url(#${goldGradId})`} strokeWidth="1.8" />
            <line x1="32" y1="25" x2="44" y2="33" stroke={`url(#${goldGradId})`} strokeWidth="1.8" />
          </g>
        );

      case 'orchestration':
      case 'workflow':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="58" rx="20" ry="4" fill={`url(#${shadowGradId})`} />
            {/* Node 1 - Top Center */}
            <polygon points="32,10 44,17 32,24 20,17" fill={`url(#${glassGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1.5" />
            <circle cx="32" cy="17" r="3.5" fill={`url(#${goldGradId})`} />
            {/* Node 2 - Bottom Left */}
            <polygon points="18,34 30,41 18,48 6,41" fill={`url(#${glassGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1.5" />
            <circle cx="18" cy="41" r="3" fill={`url(#${goldGradId})`} />
            {/* Node 3 - Bottom Right */}
            <polygon points="46,34 58,41 46,48 34,41" fill={`url(#${glassGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1.5" />
            <circle cx="46" cy="41" r="3" fill={`url(#${goldGradId})`} />
            {/* Gold Connection Rays */}
            <line x1="32" y1="24" x2="18" y2="34" stroke={`url(#${goldGradId})`} strokeWidth="2.5" strokeDasharray="4 2" />
            <line x1="32" y1="24" x2="46" y2="34" stroke={`url(#${goldGradId})`} strokeWidth="2.5" strokeDasharray="4 2" />
          </g>
        );

      case 'memory':
      case 'database':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="58" rx="20" ry="4" fill={`url(#${shadowGradId})`} />
            {/* 3D Glass Multi-Tier Server Cylinders */}
            {[40, 27, 14].map((y, idx) => (
              <g key={idx}>
                <path d={`M 14 ${y + 6} L 14 ${y + 12} C 14 ${y + 16} 22 ${y + 19} 32 ${y + 19} C 42 ${y + 19} 50 ${y + 16} 50 ${y + 12} L 50 ${y + 6} Z`} fill={`url(#${glassDeepGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1" />
                <ellipse cx="32" cy={y + 6} rx="18" ry="6" fill={`url(#${glassGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1.2" />
                {/* Gold Data Platter Rim & Status LED */}
                <ellipse cx="32" cy={y + 6} rx="15" ry="4.5" fill="none" stroke={`url(#${goldGradId})`} strokeWidth="0.8" />
                <circle cx="44" cy={y + 12} r="1.5" fill={`url(#${goldGradId})`} />
              </g>
            ))}
          </g>
        );

      case 'tools':
      case 'wrench':
      case 'settings':
      case 'administration':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="58" rx="20" ry="4" fill={`url(#${shadowGradId})`} />
            {/* 3D Glass Gear Engine */}
            <circle cx="30" cy="30" r="16" fill={`url(#${glassDeepGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="2" />
            <circle cx="30" cy="30" r="8" fill="#070A40" stroke={`url(#${cyanGradId})`} strokeWidth="1" />
            {/* Metallic Gold Wrench across Gear */}
            <g transform="rotate(45 34 34)">
              <rect x="32" y="10" width="6" height="32" rx="3" fill={`url(#${goldGradId})`} stroke="#FFF7CC" strokeWidth="0.8" />
              <circle cx="35" cy="12" r="6" fill={`url(#${goldGradId})`} />
              <circle cx="35" cy="12" r="3" fill="#070A40" />
            </g>
          </g>
        );

      case 'users':
      case 'organizations':
      case 'human':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="58" rx="22" ry="4" fill={`url(#${shadowGradId})`} />
            {/* User Head - 3D Blue Glass Sphere */}
            <circle cx="32" cy="22" r="10" fill={`url(#${glassGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1.5" />
            <ellipse cx="30" cy="18" rx="6" ry="3" fill="#FFFFFF" opacity="0.4" />
            {/* Metallic Gold Crown / Ring */}
            <ellipse cx="32" cy="16" rx="9" ry="3" fill="none" stroke={`url(#${goldGradId})`} strokeWidth="2" />
            {/* User Torso - 3D Blue Glass */}
            <path d="M 16 48 C 16 37 23 34 32 34 C 41 34 48 37 48 48 Z" fill={`url(#${glassDeepGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1.8" />
            {/* Gold Lapel Crest */}
            <polygon points="32,34 29,42 35,42" fill={`url(#${goldGradId})`} />
          </g>
        );

      case 'target':
      case 'mission':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="58" rx="20" ry="4" fill={`url(#${shadowGradId})`} />
            {/* Outer Blue Glass Target Ring */}
            <circle cx="32" cy="32" r="20" fill={`url(#${glassDeepGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="2" />
            {/* Middle Metallic Gold Ring */}
            <circle cx="32" cy="32" r="13" fill="none" stroke={`url(#${goldGradId})`} strokeWidth="3" />
            {/* Inner Cyan Bullseye */}
            <circle cx="32" cy="32" r="6" fill={`url(#${cyanGradId})`} />
            {/* Gold Bullseye Point */}
            <circle cx="32" cy="32" r="2.5" fill={`url(#${goldGradId})`} />
          </g>
        );

      case 'compass':
      case 'direction':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="58" rx="20" ry="4" fill={`url(#${shadowGradId})`} />
            {/* Compass Rim - Blue Glass with Gold Bezel */}
            <circle cx="32" cy="32" r="20" fill={`url(#${glassDeepGradId})`} stroke={`url(#${goldGradId})`} strokeWidth="2.5" />
            <circle cx="32" cy="32" r="16" fill={`url(#${glassGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1" />
            {/* 3D Metallic Gold Needle */}
            <polygon points="32,16 36,32 32,30 28,32" fill={`url(#${goldGradId})`} stroke="#FFF7CC" strokeWidth="0.8" />
            <polygon points="32,48 36,32 32,34 28,32" fill="#E63946" stroke="#FFFFFF" strokeWidth="0.8" />
            <circle cx="32" cy="32" r="3" fill={`url(#${goldGradId})`} />
          </g>
        );

      case 'lightning':
      case 'speed':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="58" rx="18" ry="4" fill={`url(#${shadowGradId})`} />
            {/* Blue Glass Backing Shield */}
            <path d="M 32 10 L 48 16 C 48 32 42 46 32 52 C 22 46 16 32 16 16 Z" fill={`url(#${glassDeepGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1.5" />
            {/* 3D Beveled Metallic Gold Lightning Bolt */}
            <polygon
              points="34,14 20,32 30,32 26,50 44,28 32,28"
              fill={`url(#${goldGradId})`}
              stroke="#FFF7CC"
              strokeWidth="1.5"
              strokeLinejoin="round"
            />
          </g>
        );

      case 'location':
      case 'geography':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="56" rx="14" ry="4" fill={`url(#${shadowGradId})`} />
            <path
              d="M 32 10 C 21 10 14 18 14 28 C 14 40 32 54 32 54 C 32 54 50 40 50 28 C 50 18 43 10 32 10 Z"
              fill={`url(#${glassGradId})`}
              stroke={`url(#${cyanGradId})`}
              strokeWidth="2"
            />
            <path d="M 32 12 C 24 12 18 18 18 26 C 24 22 30 18 32 12 Z" fill="#FFFFFF" opacity="0.4" />
            <circle cx="32" cy="26" r="8" fill={`url(#${goldGradId})`} stroke="#FFF7CC" strokeWidth="1" />
            <circle cx="32" cy="26" r="3.5" fill="#070A40" />
          </g>
        );

      case 'microscope':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="58" rx="20" ry="4" fill={`url(#${shadowGradId})`} />
            <path d="M 18 52 C 18 48 24 46 32 46 C 40 46 46 48 46 52 L 44 56 C 44 57 38 58 32 58 C 26 58 20 57 20 56 Z" fill={`url(#${glassDeepGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1.5" />
            <path d="M 40 50 C 44 42 44 26 36 20 C 32 17 28 17 26 20" fill="none" stroke={`url(#${glassGradId})`} strokeWidth="5" strokeLinecap="round" />
            <rect x="20" y="38" width="20" height="4" rx="1.5" fill={`url(#${goldGradId})`} stroke="#FFF7CC" strokeWidth="0.8" />
            <rect x="22" y="10" width="8" height="18" rx="2" transform="rotate(-20 26 19)" fill={`url(#${glassDeepGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1.5" />
            <ellipse cx="23" cy="11" rx="4" ry="2" transform="rotate(-20 23 11)" fill={`url(#${cyanGradId})`} />
            <circle cx="28" cy="30" r="4" fill={`url(#${goldGradId})`} />
            <rect x="26" y="32" width="4" height="6" fill={`url(#${goldGradId})`} stroke="#FFF7CC" strokeWidth="0.5" />
          </g>
        );

      case 'policy-shield':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="58" rx="20" ry="4" fill={`url(#${shadowGradId})`} />
            <path
              d="M 32 8 L 52 16 C 52 36 42 48 32 54 C 22 48 12 36 12 16 Z"
              fill={`url(#${glassDeepGradId})`}
              stroke={`url(#${cyanGradId})`}
              strokeWidth="2.5"
            />
            <path
              d="M 32 12 L 48 19 C 48 34 39 44 32 49 C 25 44 16 34 16 19 Z"
              fill={`url(#${glassGradId})`}
              opacity="0.85"
            />
            <line x1="32" y1="20" x2="32" y2="44" stroke={`url(#${goldGradId})`} strokeWidth="2.5" strokeLinecap="round" />
            <line x1="24" y1="44" x2="40" y2="44" stroke={`url(#${goldGradId})`} strokeWidth="2" strokeLinecap="round" />
            <line x1="20" y1="26" x2="44" y2="26" stroke={`url(#${goldGradId})`} strokeWidth="2.5" strokeLinecap="round" />
            <line x1="20" y1="26" x2="16" y2="36" stroke="#FFF7CC" strokeWidth="1" />
            <line x1="20" y1="26" x2="24" y2="36" stroke="#FFF7CC" strokeWidth="1" />
            <path d="M 14 36 Q 20 40 26 36 Z" fill={`url(#${goldGradId})`} stroke="#FFF7CC" strokeWidth="0.8" />
            <line x1="44" y1="26" x2="40" y2="36" stroke="#FFF7CC" strokeWidth="1" />
            <line x1="44" y1="26" x2="48" y2="36" stroke="#FFF7CC" strokeWidth="1" />
            <path d="M 38 36 Q 44 40 50 36 Z" fill={`url(#${goldGradId})`} stroke="#FFF7CC" strokeWidth="0.8" />
          </g>
        );

      case 'system-map':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="58" rx="22" ry="4" fill={`url(#${shadowGradId})`} />
            <polygon points="10,24 24,18 24,48 10,54" fill={`url(#${glassDeepGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1.5" />
            <polygon points="24,18 38,24 38,54 24,48" fill={`url(#${glassGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1.5" />
            <polygon points="38,24 54,18 54,48 38,54" fill={`url(#${glassDeepGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1.5" />
            <line x1="14" y1="28" x2="20" y2="50" stroke="#BAE6FD" strokeWidth="1" opacity="0.6" />
            <line x1="28" y1="26" x2="34" y2="48" stroke="#BAE6FD" strokeWidth="1" opacity="0.6" />
            <line x1="42" y1="28" x2="50" y2="46" stroke="#BAE6FD" strokeWidth="1" opacity="0.6" />
            <g transform="translate(38, 12)">
              <path d="M 0 0 C -6 0 -10 4 -10 10 C -10 18 0 26 0 26 C 0 26 10 18 10 10 C 10 4 6 0 0 0 Z" fill={`url(#${cyanGradId})`} stroke="#FFFFFF" strokeWidth="1.5" />
              <circle cx="0" cy="9" r="3.5" fill="#FFFFFF" />
            </g>
          </g>
        );

      case 'africa-map':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="58" rx="20" ry="4" fill={`url(#${shadowGradId})`} />
            <path
              d="M 22 12 C 30 10 44 12 48 18 C 52 24 50 30 46 36 C 42 42 38 52 32 54 C 28 54 26 44 24 36 C 20 34 14 30 14 24 C 14 18 18 14 22 12 Z"
              fill={`url(#${glassGradId})`}
              stroke={`url(#${cyanGradId})`}
              strokeWidth="2.2"
            />
            <path d="M 52 40 C 54 38 55 44 53 48 C 51 46 50 42 52 40 Z" fill={`url(#${cyanGradId})`} stroke="#FFFFFF" strokeWidth="0.8" />
            <path d="M 24 16 C 30 14 40 16 44 20 C 38 22 28 20 24 16 Z" fill="#FFFFFF" opacity="0.5" />
            <circle cx="32" cy="42" r="2.5" fill={`url(#${goldGradId})`} />
            <circle cx="36" cy="24" r="2" fill={`url(#${goldGradId})`} />
            <circle cx="24" cy="26" r="2" fill={`url(#${goldGradId})`} />
            <line x1="32" y1="42" x2="36" y2="24" stroke="#FFF7CC" strokeWidth="1" strokeDasharray="2 1" />
            <line x1="32" y1="42" x2="24" y2="26" stroke="#FFF7CC" strokeWidth="1" strokeDasharray="2 1" />
          </g>
        );

      case 'registration':
      case 'verification':
      case 'approvals':
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="58" rx="20" ry="4" fill={`url(#${shadowGradId})`} />
            <rect x="16" y="14" width="32" height="40" rx="5" fill={`url(#${glassGradId})`} stroke={`url(#${cyanGradId})`} strokeWidth="1.8" />
            <rect x="26" y="10" width="12" height="4" rx="2" fill={`url(#${goldGradId})`} />
            {/* Verified Gold Checkmark Medal */}
            <circle cx="32" cy="34" r="11" fill={`url(#${goldGradId})`} stroke="#FFF7CC" strokeWidth="1.2" />
            <path d="M 27 34 L 30 38 L 38 29" fill="none" stroke="#070A40" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
          </g>
        );

      case 'brand-emblem':
      default:
        return (
          <g filter={`url(#${filterId})`}>
            <ellipse cx="32" cy="58" rx="22" ry="4" fill={`url(#${shadowGradId})`} />
            {/* 3D Glass Shield Base */}
            <path
              d="M 32 8 L 52 16 C 52 34 44 48 32 54 C 20 48 12 34 12 16 Z"
              fill={`url(#${glassGradId})`}
              stroke={`url(#${cyanGradId})`}
              strokeWidth="2"
            />
            {/* 3D Polished Gold Lighthouse Beam Core */}
            <polygon points="32,20 25,44 39,44" fill={`url(#${goldGradId})`} stroke="#FFF7CC" strokeWidth="1" />
            <circle cx="32" cy="20" r="4.5" fill="#FFF7CC" stroke={`url(#${goldGradId})`} strokeWidth="1" />
            {/* Cyan Signal Waves */}
            <path d="M 23 20 A 9 9 0 0 1 41 20" fill="none" stroke={`url(#${cyanGradId})`} strokeWidth="2" strokeLinecap="round" />
            <path d="M 18 16 A 14 14 0 0 1 46 16" fill="none" stroke={`url(#${cyanGradId})`} strokeWidth="2" strokeLinecap="round" opacity="0.7" />
          </g>
        );
    }
  };

  return (
    <div
      className={`inline-flex items-center justify-center shrink-0 select-none ${
        isInteractive ? 'hover:scale-105 transition-transform duration-200 cursor-pointer' : ''
      } ${className}`}
      style={{ width: px, height: px }}
      role="img"
      aria-label={alt || `${name} 3D icon`}
    >
      <svg
        viewBox="0 0 64 64"
        width={px}
        height={px}
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="w-full h-full object-contain"
      >
        {renderDefs()}
        {renderIconContent(name)}
      </svg>
    </div>
  );
};

export default Icon3D;
