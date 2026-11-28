import React, { useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

interface ImageCarouselProps {
  images: { src: string; alt: string; caption?: string }[];
  theme: 'light' | 'dark';
}

export const ImageCarousel: React.FC<ImageCarouselProps> = ({ images, theme }) => {
  const [index, setIndex] = useState(0);
  const isLight = theme === 'light';
  const current = images[index];
  const prev = () => setIndex((i) => (i - 1 + images.length) % images.length);
  const next = () => setIndex((i) => (i + 1) % images.length);

  return (
    <section className="relative w-full overflow-hidden h-[40vh] sm:h-[48vh] lg:h-[56vh]" aria-label="Image carousel">
      <img
        src={current.src}
        alt={current.alt}
        loading="lazy"
        className="absolute inset-0 w-full h-full object-cover object-center transition-opacity duration-500"
      />
      <div
        className={`absolute inset-0 ${
          isLight
            ? 'bg-gradient-to-t from-[#F7F8F9]/60 via-transparent to-transparent'
            : 'bg-gradient-to-t from-[#0A0D14]/65 via-transparent to-transparent'
        }`}
        aria-hidden="true"
      />
      {current.caption && (
        <div className="absolute bottom-6 left-6 right-6 z-10 max-w-3xl">
          <p className={`text-sm sm:text-base font-medium ${isLight ? 'text-ls-navy' : 'text-white'}`}>
            {current.caption}
          </p>
        </div>
      )}
      <button
        type="button"
        onClick={prev}
        aria-label="Previous image"
        className="absolute left-4 top-1/2 -translate-y-1/2 z-20 rounded-full bg-black/40 hover:bg-black/60 text-white p-2"
      >
        <ChevronLeft className="w-5 h-5" />
      </button>
      <button
        type="button"
        onClick={next}
        aria-label="Next image"
        className="absolute right-4 top-1/2 -translate-y-1/2 z-20 rounded-full bg-black/40 hover:bg-black/60 text-white p-2"
      >
        <ChevronRight className="w-5 h-5" />
      </button>
      <div className="absolute bottom-4 right-6 z-20 flex gap-1.5">
        {images.map((_, i) => (
          <button
            key={i}
            type="button"
            onClick={() => setIndex(i)}
            aria-label={`Go to image ${i + 1}`}
            className={`w-2 h-2 rounded-full ${i === index ? 'bg-white' : 'bg-white/40'}`}
          />
        ))}
      </div>
    </section>
  );
};

export default ImageCarousel;
