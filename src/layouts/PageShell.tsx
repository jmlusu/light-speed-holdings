/**
 * PageShell Layout
 *
 * Root layout combining Header, PageContainer, and Footer
 * Directive §3, §9
 */

import React from 'react';
import { Outlet } from 'react-router-dom';
import { Header } from '../components/header/Header';
import { Footer } from '../components/footer/Footer';
import { PageContainer } from './PageContainer';
import { tokens } from '@lightspeed/design-system/tokens';

export const PageShell: React.FC = () => {
  const isDark = document.documentElement.classList.contains('dark');

  const shellStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    minHeight: '100vh',
    backgroundColor: isDark ? tokens.colors.deepMineral : tokens.colors.morningMist,
  };

  const mainStyle: React.CSSProperties = {
    flex: 1,
    width: '100%',
  };

  return (
    <div style={shellStyle}>
      <Header />
      <main style={mainStyle} id="main-content" role="main">
        <PageContainer>
          <Outlet />
        </PageContainer>
      </main>
      <Footer />
    </div>
  );
};

export default PageShell;
