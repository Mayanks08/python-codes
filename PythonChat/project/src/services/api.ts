export async function generateResponse(message: string) {
  try {
    const response = await fetch(import.meta.env.VITE_GEMINI_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        contents: [{
          parts: [{
            text: `You are a friendly Python tutor for children. Please explain Python concepts in a simple, fun way. User message: ${message}`
          }]
        }]
      })
    });

    const data = await response.json();
    return data.candidates[0].content.parts[0].text;
  } catch (error) {
    console.error('Error generating response:', error);
    throw new Error('Failed to generate response');
  }
}