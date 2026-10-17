with open("C:/Users/jmlus/light-speed-holdings/src/pages/WhatWeDoPage.tsx", "r") as f:
    content = f.read()

# Fix the stray return statement
old = "};\n\n  return (\n    <>\n      {/* 1. EXECUTIVE OUTCOME (Above the fold: what/who/why/next in 5s) */}"
new = '};\n\n/** Main WhatWeDoPage component */\nexport const WhatWeDoPage: React.FC<WhatWeDoPageProps> = ({ theme, onRequestBriefing }) => {\n  const isLight = theme === "light";\n  const [activeTab, setActiveTab] = useState<CatalogTab>("packages");\n\n  return (\n    <>\n      {/* 1. EXECUTIVE OUTCOME (Above the fold: what/who/why/next in 5s) */}'

new_content = content.replace(old, new)
with open("C:/Users/jmlus/light-speed-holdings/src/pages/WhatWeDoPage.tsx", "w") as f:
    f.write(new_content)
print("Fixed!")
