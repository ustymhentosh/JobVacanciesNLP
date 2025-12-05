## Instruction


### Tags
| Category                     | Tag                | Description                                                                    | Example(s)                                                                                |
| ---------------------------- | ------------------ | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| **Hard Skills**              | `SKILL_HARD`       | Specific technical tools, programming languages, frameworks, or methodologies. | “Python”, “React.js”, “Docker”, “machine learning”, “REST API”, “CI/CD”                   |
| **Soft Skills**              | `SKILL_SOFT`       | Personal, communication, or team-related skills.                               | “problem-solving”, “team player”, “attention to detail”, “leadership”                     |
| **English Level**            | `ENGLISH_LEVEL`    | Any explicit or implied English proficiency level.                             | “Upper-Intermediate”, “fluent English”, “B2 level”, “advanced English communication”      |
| **Education Level / Degree** | `DEGREE`           | Formal education requirements or mentions of degree type.                      | “Bachelor’s degree”, “Master’s in Computer Science”, “PhD in Engineering”                 |
| **Experience Level**         | `EXPERIENCE_LEVEL` | Seniority or role level mentioned.                                             | “Junior”, “Middle”, “Senior”, “Lead”, “Intern”, “Principal Engineer”                      |
| **Experience Duration**      | `EXPERIENCE_YEARS` | Required or mentioned years of experience.                                     | “3+ years of experience”, “at least two years working with Python”                        |
| **Job Benefits**             | `BENEFIT`          | Offered perks, bonuses, and work conditions.                                   | “medical insurance”, “flexible schedule”, “remote work”, “paid vacation”, “stock options” |
| **Location**                 | `LOCATION`         | Mention of workplace location or remote setting.                               | “Kyiv”, “Lviv”, “remote”, “Poland”                                                        |
| **Company Name**             | `COMPANY`          | Employer or recruiter company name.                                            | “EPAM Systems”, “SoftServe”, “Google”                                                     |
| **Position / Role Title**    | `ROLE`             | Job title or target position.                                                  | “Frontend Developer”, “DevOps Engineer”, “Data Scientist”                                 |

### Guidelines
| Rule                  | Description                                                                                                                                                                                                                                                           |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Granularity:**      | Label **only the minimal, complete phrase** that expresses the entity. Don’t include extra words like articles or adjectives unless part of the name (e.g., “Senior Backend Developer” → tag only “Backend Developer” as `ROLE`, and “Senior” as `EXPERIENCE_LEVEL`). |
| **Consistency:**      | Use **the same label for the same phrase** across all documents (e.g., always tag “Upper-Intermediate English” as `ENGLISH_LEVEL`, not `SKILL_SOFT`).                                                                                                                 |
| **No Overlaps:**      | If an entity can fall under multiple tags, choose the **most specific** one (e.g., “communication skills” → `SKILL_SOFT`, not `ENGLISH_LEVEL`).                                                                                                                       |
| **Whole Words Only:** | Don’t tag partial words. Tag the full expression like “REST API” not just “API”.                                                                                                                                                                                      |
| **Context Matters:**  | Use context to disambiguate — “Python” in “Python script” → `SKILL_HARD`; “Python course” → still `SKILL_HARD`.                                                                                                                                                       |
| **Case-Insensitive:** | Tag regardless of capitalization.                                                                                                                                                                                                                                     |
| **Duplicates:**       | Tag all mentions, even repeated ones in the same text.                                                                                                                                                                                                                |
### WORK SPLIT
Ustym - 30 Python<br>
Dmytro - 30 AIML