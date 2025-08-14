
import { useState, useEffect, useRef } from 'react';
import { Mic, MicOff,  RotateCw,  Volume2,  Zap } from 'lucide-react';
import { io, Socket } from 'socket.io-client';

// Check for browser's SpeechRecognition API
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = SpeechRecognition ? new SpeechRecognition() : null;

if (recognition) {
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = 'en-US';
}

interface Message {
  id: string;
  type: 'user' | 'ai';
  text: string;
  timestamp: number;
}

interface VoiceState {
  isRecording: boolean;
  isPlaying: boolean;
  isConnected: boolean;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [voiceState, setVoiceState] = useState<VoiceState>({
    isRecording: false,
    isPlaying: false,
    isConnected: false
  });
  const [apiKey, setApiKey] = useState(localStorage.getItem('gemini_api_key') || '');
 const [connectionStatus, setConnectionStatus] = useState<'disconnected' | 'connecting' | 'connected'>('disconnected');
  
  const socketRef = useRef<Socket | null>(null);
  const transcriptRef = useRef<HTMLDivElement>(null);

  // Speak text using the browser's TTS API
  const speakText = (text: string) => {
    // Cancel any ongoing speech
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.onstart = () => setVoiceState(prev => ({ ...prev, isPlaying: true }));
    utterance.onend = () => setVoiceState(prev => ({ ...prev, isPlaying: false }));
    utterance.onerror = () => setVoiceState(prev => ({ ...prev, isPlaying: false }));
    
    window.speechSynthesis.speak(utterance);
  };

  // Initialize socket connection
  useEffect(() => {
    setConnectionStatus('connecting');
    socketRef.current = io('http://localhost:3001', {
      transports: ['websocket', 'polling'],
      withCredentials: true,
    });
    const socket = socketRef.current;

    socket.on('connect', () => {
      console.log('Frontend connected:', socket.id);
      setConnectionStatus('connected');
      setVoiceState(prev => ({ ...prev, isConnected: true }));
    });
    
    // Listen for the AI's text response from the server
    socket.on('ai-response-text', (data: { text: string }) => {
      const newMessage: Message = {
        id: Date.now().toString() + '-ai',
        type: 'ai',
        text: data.text,
        timestamp: Date.now()
      };
      setMessages(prev => [...prev, newMessage]);
      speakText(data.text);
    });

    socket.on('connect_error', () => setConnectionStatus('disconnected'));
    socket.on('disconnect', () => setConnectionStatus('disconnected'));
    socket.on('error', (error: { message: string }) => console.error('Socket error:', error));

    return () => {
      socket.disconnect();
      window.speechSynthesis.cancel();
    };
  }, []);

  const startRecording = () => {
    if (!recognition) {
        alert("Speech Recognition is not supported in this browser. Please use Google Chrome.");
        return;
    }
    if (voiceState.isRecording || !voiceState.isConnected) return;
    
    setVoiceState(prev => ({ ...prev, isRecording: true }));

    recognition.onresult = (event) => {
      let finalTranscript = '';
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript;
        }
      }

      if (finalTranscript) {
        const newMessage: Message = {
          id: Date.now().toString() + '-user',
          type: 'user',
          text: finalTranscript,
          timestamp: Date.now()
        };
        setMessages(prev => [...prev, newMessage]);

        // Send the final transcript to the backend
        if (socketRef.current) {
          socketRef.current.emit('text-input', {
            transcript: finalTranscript,
            apiKey: apiKey || undefined
          });
        }
      }
    };
    
    recognition.start();
  };

  const stopRecording = () => {
    if (recognition && voiceState.isRecording) {
      recognition.stop();
      setVoiceState(prev => ({ ...prev, isRecording: false }));
    }
  };

  const interruptAI = () => {
   window.speechSynthesis.cancel(); 
  
   window.speechSynthesis.resume(); 
   setVoiceState(prev => ({ ...prev, isPlaying: false }))
  };


  const restartConversation = () => {
  
  window.speechSynthesis.cancel();
  
 
  setMessages([]);
  
  setVoiceState(prev => ({ ...prev, isPlaying: false, isRecording: false }));
  }
  
  
  
  return (
    
    <div className="min-h-screen  bg-gradient-to-br from-green-900 via-blue-900 to-green-900">
        {/* Header */}
        <div className="bg-black/20 backdrop-blur-sm border-b border-white/10">
            <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg">
                    <Zap className="w-6 h-6 text-white" />
                </div>
                <div>
                    <h1 className="text-xl font-bold text-white">Revolt Motors</h1>
                    <p className="text-sm text-gray-300">Voice Assistant</p>
                </div>
                </div>
            </div>
            </div>
        </div>


        <div className="container mx-auto p-4 max-w-6x ">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-140px)]">
            
           
            <div className="bg-black/20 backdrop-blur-sm border border-white/20 rounded-xl p-6 flex flex-col justify-center items-center">
                <h2 className="text-xl font-semibold text-white mb-6">Voice Controls</h2>
                
                
                <div className="relative mb-8">
                <button
                    className={`w-24 h-24 rounded-full flex items-center justify-center transition-all duration-200 ${
                        voiceState.isRecording 
                        ? 'bg-red-500 animate-pulse shadow-lg shadow-red-500/50' 
                        : voiceState.isConnected 
                            ? 'bg-blue-600 hover:bg-blue-700 shadow-lg shadow-blue-500/30' 
                            : 'bg-gray-600 cursor-not-allowed'
                    }`}
                    onMouseDown={startRecording}
                    onMouseUp={stopRecording}
                    onTouchStart={startRecording}
                    onTouchEnd={stopRecording}
                    disabled={!voiceState.isConnected || voiceState.isPlaying}
                >
                    {voiceState.isRecording ? 
                    <MicOff className="w-10 h-10 text-white" /> : 
                    <Mic className="w-10 h-10 text-white" />
                    }
                </button>
                {voiceState.isRecording && (
                    <div className="absolute inset-0 rounded-full border-4 border-red-400 animate-ping"></div>
                )}
                </div>

                <p className="text-gray-300 mb-6 h-10 text-center">
                    {voiceState.isPlaying ? 'AI is speaking...' : voiceState.isRecording ? 'Recording... Release to send' : 'Hold to speak'}
                </p>

               
                {voiceState.isPlaying && (
                <div className="flex items-center justify-center gap-2 mb-6 p-3 bg-purple-500/20 rounded-lg w-full">
                    <Volume2 className="w-5 h-5 text-purple-400 animate-pulse" />
                    <span className="text-purple-300">AI is speaking...</span>
                </div>
                )}

                <div className="space-y-3 w-full">
                {voiceState.isPlaying && (
                    <button
                        className="w-full px-4 py-2 bg-yellow-600 hover:bg-yellow-700 text-white rounded-lg transition-colors"
                        onClick={interruptAI}
                    >
                    Interrupt AI
                    </button>
                )}
                
                <button
                  className="w-full px-4 py-2 bg-blue-600 hover:bg-gray-700 text-white rounded-lg transition-colors flex items-center justify-center gap-2"
                  onClick={restartConversation}
                >
                  <RotateCw className="w-4 h-4" />
                  Restart Conversation
                </button>
                </div>
            </div>

          
            
            </div>
        </div>
    </div>
  );
}

export default App;