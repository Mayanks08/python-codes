import { GoogleGenerativeAI } from '@google/generative-ai';

export class GeminiService {
  constructor() {
    this.apiKey = process.env.GEMINI_API_KEY;
    this.genAI = null;
    this.model = null;
    
    if (this.apiKey) {
      this.initializeModel();
    }
  }

  // initializeModel() {
  //   try {
  //     this.genAI = new GoogleGenerativeAI(this.apiKey);
  //    this.model = this.genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
  //     console.log('Gemini AI initialized successfully');
  //   } catch (error) {
  //     console.error('Failed to initialize Gemini AI:', error);
  //   }
  // }

  initializeModel() {
  try {
    this.genAI = new GoogleGenerativeAI(this.apiKey);

    // --- FROM THIS ---
    // this.model = this.genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

    // --- TO THIS ---
    // const instruction = "You are a helpful AI assistant for Revolt Motors, an electric motorcycle company.  You should only discuss topics related to Revolt Motors, their electric motorcycles, specifications, features, pricing, availability, and general electric vehicle topics. If asked about unrelated topics, politely redirect the conversation back to Revolt Motors and electric motorcycles. Keep responses conversational and helpful, as if you're speaking to a potential customer.";
    const instruction = `You are an enthusiastic and knowledgeable AI voice assistant for Revolt Motors. Your primary source of truth is the official website: https://www.revoltmotors.com/.

    Your goal is to answer questions about Revolt's products, features, and pricing based *only* on the information from that website. Be helpful and guide users towards booking a test ride.

    If a user asks about unrelated topics (like competitors), politely state that you're a specialist for Revolt Motors and redirect the conversation back to their bikes. Keep your answers conversational and concise for a voice-first interface.`;
    
    this.model = this.genAI.getGenerativeModel({ 
      model: "gemini-1.5-flash",
      systemInstruction: instruction,
    });

    console.log('Gemini AI initialized successfully with a system prompt.');
  } catch (error) {
    console.error('Failed to initialize Gemini AI:', error);
  }
}

  updateApiKey(apiKey) {
    this.apiKey = apiKey;
    this.initializeModel();
  }

  async generateResponse(prompt) {
    if (!this.model) {
      return "Please configure your Gemini API key in the settings to enable AI responses.";
    }

    try {
      const result = await this.model.generateContent(prompt);
      const response = await result.response;
      return response.text();
    } catch (error) {
      console.error('Error generating response:', error);
      
      if (error.message.includes('API_KEY_INVALID')) {
        return "Invalid API key. Please check your Gemini API key in the settings.";
      } else if (error.message.includes('QUOTA_EXCEEDED')) {
        return "API quota exceeded. Please check your Gemini API usage limits.";
      } else {
        return "Sorry, I encountered an error while processing your request. Please try again.";
      }
    }
  }
}