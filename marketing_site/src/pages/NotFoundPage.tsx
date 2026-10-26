/**
 * NotFoundPage — real 404 (mission Requirement F).
 *
 * Replaces the former catch-all <Navigate to="/"> redirect so unknown URLs
 * return genuine not-found content (correct for users and crawlers).
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { PageContainer } from '../layouts/PageContainer';
import { Section, Heading, Text, Stack } from '@lightspeed/design-system';
import { tokens } from '@lightspeed/design-system/tokens';

export const NotFoundPage: React.FC = () => {
  const isDark = document.documentElement.classList.contains('dark');

  return (
    <PageContainer>
      <Section label="404" theme={isDark ? 'dark' : 'light'}>
        <div style={{ textAlign: 'center', maxWidth: '720px', margin: '0 auto' }}>
          <Heading level={1} style={{ marginBottom: tokens.spacing[4] }}>
            Page not found
          </Heading>
          <Text variant="lead" style={{ marginBottom: tokens.spacing[8] }}>
            The page you are looking for does not exist or has moved.
          </Text>
          <Stack direction="horizontal" gap={3} justify="center" wrap>
            <Link
              to="/"
              className={`px-6 py-3.5 rounded-full font-bold text-xs tracking-widest transition-all shadow-xs flex items-center gap-2 cursor-pointer ${
                isDark
                  ? 'bg-ls-red hover:bg-ls-red text-ls-white'
                  : 'bg-ls-navy hover:bg-ls-navy text-ls-white'
              }`}
            >
              <span>Back to home</span>
            </Link>
            <Link
              to="/contact"
              className={`px-6 py-3.5 rounded-full font-bold text-xs tracking-widest border transition-all shadow-xs flex items-center gap-2 cursor-pointer ${
                isDark
                  ? 'bg-ls-navy/80 hover:bg-ls-navy text-ls-grey-light-text hover:text-ls-white border-ls-white/15'
                  : 'bg-ls-white hover:bg-ls-grey-light text-ls-navy border-ls-grey-dark hover:border-ls-red'
              }`}
            >
              <span>Contact us</span>
            </Link>
          </Stack>
        </div>
      </Section>
    </PageContainer>
  );
};

export default NotFoundPage;
