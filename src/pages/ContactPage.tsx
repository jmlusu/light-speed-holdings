import React from 'react';
import { ContactSection } from '../components/ContactSection';
import { FaqSection } from '../components/site/FaqSection';

interface ContactPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const ContactPage: React.FC<ContactPageProps> = ({ theme }) => {
  return (
    <>
      <ContactSection theme={theme} />
      <FaqSection theme={theme} />
    </>
  );
};

export default ContactPage;
