
import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import cors from 'cors';
import dotenv from 'dotenv';
import { GeminiService } from './gemini-service.js';

dotenv.config();

const app = express();
const server = createServer(app);
const io = new Server(server, {
  cors: {
    origin: "http://localhost:5173",
    methods: ["GET", "POST"],
    credentials: true
  }
});

app.use(cors());
app.use(express.json());

const geminiService = new GeminiService();

io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);

  // Listen for text input from the client
  socket.on('text-input', async (data) => {
    try {
      const { transcript, apiKey } = data;
      console.log('Received text:', transcript);

      if (apiKey) {
        geminiService.updateApiKey(apiKey);
      }

      // 1. Send text to Gemini and get a response
      const aiResponseText = await geminiService.generateResponse(transcript);

      // 2. Emit the AI's text response back to the client
      socket.emit('ai-response-text', { text: aiResponseText });

    } catch (error) {
      console.error('Error processing text input:', error);
      socket.emit('error', { message: `Server error: ${error.message}` });
    }
  });

  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
  });
});

const PORT = process.env.PORT || 3001;

server.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});