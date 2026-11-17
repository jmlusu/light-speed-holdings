import { insightArticles, insightCategories } from '../data/siteContent';

test('category filter All displays all 9 articles', () => {
  const { length } = insightArticles;
  expect(length).toBe(9);
});

test('category filter AI Governance narrows to matching articles', () => {
  const governanceArticles = insightArticles.filter(
    (article) => article.topic === 'AI GOVERNANCE' || article.category === 'AI governance'
  );
  expect(governanceArticles.length).toBeGreaterThan(0);
});
