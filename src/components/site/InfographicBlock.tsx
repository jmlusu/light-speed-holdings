import React from 'react';

interface InfographicBlockProps {
  theme: 'light' | 'dark';
  title: string;
  items: { label: string; value: string; image: string }[];
}

export const InfographicBlock: React.FC<InfographicBlockProps> = ({ theme, title, items }) => {
  const isLight = theme === 'light';
  return (
    <section className={`px-6 lg:px-12 py-16 ${isLight ? 'bg-[#F7F8F9]' : 'bg-[#0A0D14]'}`}>
      <div className="max-w-7xl mx-auto">
        <h2 className={`text-2xl sm:text-3xl font-bold mb-8 ${isLight ? 'text-ls-navy' : 'text-white'}`}>{title}</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {items.map((item) => (
            <div key={item.label} className={`rounded-lg overflow-hidden ${isLight ? 'bg-white' : 'bg-white/5'}`}>
              <img src={item.image} alt={item.label} loading="lazy" className="w-full h-40 object-cover" />
              <div className="p-4">
                <p className={`text-xs uppercase tracking-widest ${isLight ? 'text-ls-navy/60' : 'text-white/60'}`}>{item.label}</p>
                <p className={`text-lg font-bold ${isLight ? 'text-ls-navy' : 'text-white'}`}>{item.value}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default InfographicBlock;
