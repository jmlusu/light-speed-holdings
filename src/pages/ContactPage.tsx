import React from 'react';
import { ContactSection } from '../components/ContactSection';

interface ContactPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const ContactPage: React.FC<ContactPageProps> = ({ theme }) => {
  return (
    <ContactSection theme={theme} />
  );
};

export default ContactPage;
