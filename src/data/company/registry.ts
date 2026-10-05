import raw from '../registries/company-registry.json';

export interface CompanyIdentity {
  name: string;
  tagline: string;
  description: string;
  founded: string;
  location: string;
  website: string;
}

export const companyIdentity = raw.company as CompanyIdentity;
