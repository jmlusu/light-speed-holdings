import React from 'react';
import { ContactSection } from '../components/ContactSection';
import { FaqSection } from '../components/site/FaqSection';
import { BigImageSection } from '../components/site/BigImageSection';

interface ContactPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const ContactPage: React.FC<ContactPageProps> = ({ theme }) => {
    {/*
     * AGENT TEAM NARRATIVE - ContactPage
     * Content fidelity governed by:
     *   - content-writer      | CTA messaging, contact form copy, and briefing prompts
     *   - data-privacy-owner  | GDPR and Malawi DPA compliance for visitor data collection
     * Last audited: 2026-10-18
     */}
  return (
    <>
      <BigImageSection theme={theme} src="/assets/aistudio/call_to_action_blank_background_ee1fa8f8.jpg" alt="Contact" caption="Let's build together." />
      <ContactSection theme={theme} />
      <FaqSection theme={theme} />
    </>
  );
};

export default ContactPage;
