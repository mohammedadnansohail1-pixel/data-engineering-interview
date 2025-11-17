# Contributing to Data Engineering Interview Prep Platform

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Adding Questions](#adding-questions)

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Respect different viewpoints and experiences

## Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/data-engineering-interview.git
   cd data-engineering-interview
   ```

2. **Set up development environment**
   ```bash
   # Quick setup
   ./setup.sh

   # Or manually
   docker-compose up -d
   docker-compose exec backend python app/seed_questions.py
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Backend Development

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run with auto-reload
uvicorn app.main:app --reload

# Format code
black app/
ruff check app/

# Type checking
mypy app/
```

### Frontend Development

```bash
# Install dependencies
cd frontend
npm install

# Run development server
npm run dev

# Run tests
npm test

# Lint code
npm run lint

# Format code
npm run format
```

## Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints for function signatures
- Write docstrings for functions and classes
- Maximum line length: 100 characters
- Use meaningful variable names

```python
# Good
def calculate_average_score(attempts: List[Attempt]) -> float:
    """Calculate the average score from a list of attempts."""
    if not attempts:
        return 0.0
    return sum(a.score for a in attempts) / len(attempts)

# Bad
def calc(x):
    return sum(x)/len(x)
```

### TypeScript/React (Frontend)

- Use TypeScript for type safety
- Follow React best practices and hooks patterns
- Use functional components
- Keep components small and focused
- Use meaningful component and variable names

```typescript
// Good
interface QuestionCardProps {
  question: Question;
  onSelect: (id: string) => void;
}

const QuestionCard: React.FC<QuestionCardProps> = ({ question, onSelect }) => {
  return (
    <div onClick={() => onSelect(question.id)}>
      <h3>{question.title}</h3>
    </div>
  );
};

// Bad
const QCard = (props: any) => <div onClick={props.onClick}>{props.q.t}</div>;
```

## Testing

### Backend Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run only failed tests
pytest --lf
```

All PRs must include tests for new features.

### Frontend Tests

```bash
# Run tests
npm test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm test -- --watch
```

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/add-spark-questions
   ```

2. **Make your changes**
   - Write clear, concise code
   - Add tests for new features
   - Update documentation if needed
   - Follow coding standards

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add 10 new Spark interview questions"
   ```

4. **Push to your fork**
   ```bash
   git push origin feature/add-spark-questions
   ```

5. **Create a Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues
   - Include screenshots for UI changes
   - Ensure all tests pass
   - Request review from maintainers

### PR Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Code follows style guidelines
- [ ] All tests passing
- [ ] No console warnings/errors

## Screenshots (if applicable)
Add screenshots for UI changes
```

## Adding Questions

To add new interview questions:

1. **Edit the seed file**
   ```bash
   vim backend/app/seed_questions.py
   ```

2. **Add your question**
   ```python
   {
       "title": "Your Question Title",
       "description": """Question description with requirements and examples.""",
       "category": "sql",  # sql, python, spark, system_design, behavioral
       "difficulty": "medium",  # easy, medium, hard
       "question_type": "coding",  # coding, design, behavioral
       "starter_code": "SELECT -- Your starter code",
       "test_cases": {},  # Optional test cases
       "companies": ["Google", "Amazon"],
       "tags": ["sql", "joins", "aggregation"]
   }
   ```

3. **Test the question**
   ```bash
   # Clear database and reseed
   docker-compose exec backend python -c "from app.core.database import engine, Base; Base.metadata.drop_all(engine)"
   docker-compose exec backend python app/seed_questions.py
   ```

4. **Verify in the app**
   - Browse to http://localhost:3000/questions
   - Find your question and test it

## Areas for Contribution

We welcome contributions in these areas:

### High Priority
- [ ] More interview questions (especially system design)
- [ ] Additional test coverage
- [ ] Performance improvements
- [ ] Bug fixes
- [ ] Documentation improvements

### Medium Priority
- [ ] UI/UX enhancements
- [ ] Mobile responsiveness improvements
- [ ] Accessibility improvements (a11y)
- [ ] Internationalization (i18n)

### Future Features
- [ ] WebSocket support for real-time features
- [ ] Video recording functionality
- [ ] Peer practice matching
- [ ] Company-specific question packs
- [ ] Resume review system
- [ ] System design whiteboard tool

## Getting Help

- Check existing issues and PRs
- Read the documentation (README, QUICKSTART, DEPLOYMENT)
- Ask questions in GitHub Discussions
- Join our community chat (if available)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Data Engineering Interview Prep! Your efforts help developers succeed in their interviews. 🚀
