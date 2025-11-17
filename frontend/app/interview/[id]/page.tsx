'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import dynamic from 'next/dynamic';
import Navbar from '@/components/Navbar';
import { useAuth } from '@/hooks/useAuth';
import { questionsAPI, practiceAPI } from '@/lib/api';
import { getDifficultyColor } from '@/lib/utils';

// Dynamically import Monaco Editor to avoid SSR issues
const MonacoEditor = dynamic(() => import('@monaco-editor/react'), {
  ssr: false,
  loading: () => <div className="h-full flex items-center justify-center">Loading editor...</div>,
});

interface Question {
  id: string;
  title: string;
  description: string;
  category: string;
  difficulty: string;
  starter_code?: string;
  test_cases?: any;
}

export default function InterviewPage() {
  const params = useParams();
  const router = useRouter();
  const { isAuthenticated, isLoading: authLoading, checkAuth } = useAuth();
  const [question, setQuestion] = useState<Question | null>(null);
  const [code, setCode] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [feedback, setFeedback] = useState<any>(null);
  const [hintNumber, setHintNumber] = useState(0);
  const [hint, setHint] = useState('');
  const [showHint, setShowHint] = useState(false);
  const [executionResult, setExecutionResult] = useState<any>(null);

  useEffect(() => {
    checkAuth();
  }, []);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/auth/login');
    }
  }, [isAuthenticated, authLoading, router]);

  useEffect(() => {
    if (isAuthenticated && params.id) {
      loadQuestion(params.id as string);
    }
  }, [isAuthenticated, params.id]);

  const loadQuestion = async (id: string) => {
    try {
      setIsLoading(true);
      const response = await questionsAPI.get(id);
      setQuestion(response.data);
      setCode(response.data.starter_code || getDefaultCode(response.data.category));

      // Start attempt
      await practiceAPI.start(id);
    } catch (error) {
      console.error('Failed to load question:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getDefaultCode = (category: string): string => {
    if (category === 'sql') {
      return '-- Write your SQL query here\nSELECT \n  \nFROM \n';
    } else if (category === 'python' || category === 'spark') {
      return '# Write your Python code here\ndef solution():\n    pass\n';
    }
    return '// Write your code here\n';
  };

  const getLanguage = (category: string): string => {
    if (category === 'sql') return 'sql';
    if (category === 'python' || category === 'spark') return 'python';
    return 'python';
  };

  const handleSubmit = async () => {
    if (!question) return;

    setIsSubmitting(true);
    setFeedback(null);
    setExecutionResult(null);

    try {
      const response = await practiceAPI.submit(
        question.id,
        code,
        getLanguage(question.category)
      );

      setExecutionResult(response.data.execution_result);
      setFeedback(response.data.ai_feedback);
    } catch (error: any) {
      console.error('Submission failed:', error);
      setFeedback({
        score: 0,
        strengths: [],
        improvements: ['Submission failed. Please check your code and try again.'],
        optimization_suggestion: error.response?.data?.detail || 'Error occurred',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleGetHint = async () => {
    if (!question) return;

    const nextHintNumber = hintNumber + 1;
    if (nextHintNumber > 3) {
      setHint('No more hints available. Try solving the problem on your own!');
      setShowHint(true);
      return;
    }

    try {
      const response = await practiceAPI.getHint(question.id, code, nextHintNumber);
      setHint(response.data.hint);
      setHintNumber(nextHintNumber);
      setShowHint(true);
    } catch (error) {
      console.error('Failed to get hint:', error);
    }
  };

  if (authLoading || isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-pulse text-xl">Loading...</div>
      </div>
    );
  }

  if (!isAuthenticated || !question) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Navbar />

      <div className="flex-1 flex flex-col lg:flex-row">
        {/* Question Panel */}
        <div className="lg:w-1/2 bg-white border-r border-gray-200 overflow-y-auto">
          <div className="p-6">
            <div className="mb-4">
              <button
                onClick={() => router.push('/questions')}
                className="text-sm text-blue-600 hover:text-blue-700 mb-4"
              >
                ← Back to Questions
              </button>
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                {question.title}
              </h1>
              <div className="flex items-center gap-2">
                <span
                  className={`px-2 py-1 text-xs rounded-full font-medium ${getDifficultyColor(
                    question.difficulty
                  )}`}
                >
                  {question.difficulty}
                </span>
                <span className="px-2 py-1 text-xs rounded-full bg-blue-50 text-blue-700 font-medium">
                  {question.category}
                </span>
              </div>
            </div>

            <div className="prose max-w-none">
              <h3 className="text-lg font-semibold mb-2">Description</h3>
              <p className="text-gray-700 whitespace-pre-wrap">
                {question.description}
              </p>
            </div>

            {/* Hint Section */}
            {showHint && (
              <div className="mt-6 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <h3 className="text-sm font-semibold text-yellow-800 mb-2">
                  Hint {hintNumber}/3
                </h3>
                <p className="text-sm text-yellow-900">{hint}</p>
              </div>
            )}

            {/* Execution Results */}
            {executionResult && (
              <div className="mt-6 bg-gray-50 border border-gray-200 rounded-lg p-4">
                <h3 className="text-sm font-semibold text-gray-800 mb-2">
                  Test Results
                </h3>
                <div className="text-sm">
                  <p className="mb-1">
                    <span className="font-medium">Passed:</span>{' '}
                    <span className="text-green-600">{executionResult.passed}</span>
                  </p>
                  <p className="mb-1">
                    <span className="font-medium">Failed:</span>{' '}
                    <span className="text-red-600">{executionResult.failed}</span>
                  </p>
                  <p>
                    <span className="font-medium">Total:</span> {executionResult.total}
                  </p>
                </div>
                {executionResult.errors && executionResult.errors.length > 0 && (
                  <div className="mt-2">
                    <p className="font-medium text-red-600 text-sm">Errors:</p>
                    <ul className="list-disc list-inside text-sm text-red-800">
                      {executionResult.errors.map((error: string, i: number) => (
                        <li key={i}>{error}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            {/* AI Feedback */}
            {feedback && (
              <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h3 className="text-lg font-semibold text-blue-900 mb-2">
                  AI Feedback (Score: {feedback.score}/100)
                </h3>

                {feedback.strengths && feedback.strengths.length > 0 && (
                  <div className="mb-3">
                    <p className="text-sm font-medium text-green-700 mb-1">
                      Strengths:
                    </p>
                    <ul className="list-disc list-inside text-sm text-gray-700">
                      {feedback.strengths.map((strength: string, i: number) => (
                        <li key={i}>{strength}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {feedback.improvements && feedback.improvements.length > 0 && (
                  <div className="mb-3">
                    <p className="text-sm font-medium text-orange-700 mb-1">
                      Areas for Improvement:
                    </p>
                    <ul className="list-disc list-inside text-sm text-gray-700">
                      {feedback.improvements.map((improvement: string, i: number) => (
                        <li key={i}>{improvement}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {feedback.optimization_suggestion && (
                  <div>
                    <p className="text-sm font-medium text-blue-700 mb-1">
                      Optimization Suggestion:
                    </p>
                    <p className="text-sm text-gray-700">
                      {feedback.optimization_suggestion}
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Code Editor Panel */}
        <div className="lg:w-1/2 flex flex-col bg-gray-900">
          <div className="bg-gray-800 px-4 py-2 flex items-center justify-between">
            <span className="text-sm text-gray-300">Code Editor</span>
            <div className="flex gap-2">
              <button
                onClick={handleGetHint}
                disabled={hintNumber >= 3}
                className="px-3 py-1 bg-yellow-600 text-white text-sm rounded hover:bg-yellow-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Get Hint ({hintNumber}/3)
              </button>
              <button
                onClick={handleSubmit}
                disabled={isSubmitting}
                className="px-4 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSubmitting ? 'Submitting...' : 'Submit Code'}
              </button>
            </div>
          </div>

          <div className="flex-1 min-h-0">
            <MonacoEditor
              height="100%"
              language={getLanguage(question.category)}
              theme="vs-dark"
              value={code}
              onChange={(value) => setCode(value || '')}
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                lineNumbers: 'on',
                scrollBeyondLastLine: false,
                automaticLayout: true,
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
