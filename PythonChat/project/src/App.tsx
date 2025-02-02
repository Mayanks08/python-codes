import React, { useState } from 'react';
import { Bot, Settings, Send, KeyRound, Sparkles } from 'lucide-react';
import { generateResponse } from './services/api';

function App() {
  const [message, setMessage] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [showSettings, setShowSettings] = useState(false);
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant', content: string }>>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim() || isLoading) return;

    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: message }]);
    setIsLoading(true);
    
    try {
      const response = await generateResponse(message);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: "I'm sorry, I had trouble generating a response. Please try again!"
      }]);
    } finally {
      setIsLoading(false);
      setMessage('');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-5xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <Bot className="w-8 h-8 text-purple-600" />
            <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              PythonPal
            </h1>
          </div>
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <Settings className="w-6 h-6 text-gray-600" />
          </button>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-8">
        {/* Welcome Section */}
        {messages.length === 0 && (
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">
              Welcome to PythonPal! 🐍
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto mb-4">
              Your friendly AI tutor that makes learning Python fun and easy! Whether you're just starting out or working on your coding projects, I'm here to help you understand Python concepts, debug your code, and guide you through your learning journey.
            </p>
            <p className="text-gray-600 max-w-2xl mx-auto">
              With interactive lessons, real-time code explanations, and fun challenges, you'll be coding like a pro in no time! Ask me anything about Python - from basic concepts to cool project ideas. I'll adapt my explanations to your level and make sure you're having fun while learning.
            </p>
          </div>
        )}

        {/* Chat Section */}
        <div className="bg-white rounded-lg shadow-lg p-4 mb-4 min-h-[400px] flex flex-col">
          <div className="flex-1 overflow-y-auto space-y-4 mb-4">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${
                  msg.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`max-w-[80%] p-3 rounded-lg ${
                    msg.role === 'user'
                      ? 'bg-purple-600 text-white'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 text-gray-800 p-3 rounded-lg">
                  Thinking...
                </div>
              </div>
            )}
          </div>

          <form onSubmit={handleSubmit} className="flex gap-2">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Ask me anything about Python!"
              className="flex-1 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-600"
              disabled={isLoading}
            />
            <button
              type="submit"
              className={`px-4 py-2 rounded-lg flex items-center gap-2 ${
                isLoading
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-purple-600 hover:bg-purple-700'
              } text-white transition-colors`}
              disabled={isLoading}
            >
              <Send className="w-4 h-4" />
              Send
            </button>
          </form>
        </div>

        {/* Features Section */}
        <div className="grid md:grid-cols-3 gap-6 mt-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <Bot className="w-8 h-8 text-purple-600 mb-4" />
            <h3 className="text-lg font-semibold mb-2">Personalized Learning</h3>
            <p className="text-gray-600">
              Learn at your own pace with explanations tailored to your level
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <Sparkles className="w-8 h-8 text-purple-600 mb-4" />
            <h3 className="text-lg font-semibold mb-2">Interactive Challenges</h3>
            <p className="text-gray-600">
              Practice with fun coding challenges and get instant feedback
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <KeyRound className="w-8 h-8 text-purple-600 mb-4" />
            <h3 className="text-lg font-semibold mb-2">Safe Learning</h3>
            <p className="text-gray-600">
              A secure environment to experiment and learn Python programming
            </p>
          </div>
        </div>
      </main>

      {/* Settings Modal */}
      {showSettings && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white p-6 rounded-lg w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Settings</h2>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                API Key
              </label>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-purple-600"
                placeholder="Enter your API key"
              />
            </div>
            <div className="flex justify-end">
              <button
                onClick={() => setShowSettings(false)}
                className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700 transition-colors"
              >
                Save
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;