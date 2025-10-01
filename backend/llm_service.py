import os
import openai
from dotenv import load_dotenv
import logging

# One Minute... Increasing Power Levels,... Zing zing zing...   Loading environment variables
load_dotenv()

# Configuring the  logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        self.model = "gpt-3.5-turbo"
        
        # Enhanced system prompt for better responses
        self.system_prompt = """You are Mohur, a highly experienced professional AI assistant specializing in:

        LLM's CORE EXPERTISE:
        • Professional Development & Career Advancement
        • Remote Work Optimization & Team Management  
        • Leadership Skills & Management Strategies
        • Productivity Systems & Time Management
        • Work-Life Balance & Stress Management
        • Startup Growth & Business Strategy
        • Technical Team Building & Code Quality

        RESPONSE GUIDELINES:
        1. Keep responses focused and actionable (2-4 concise sentences)
        2. Provide specific, practical advice with real examples
        3. Use bullet points or numbered lists when listing multiple tips
        4. Reference proven frameworks or methodologies when relevant
        5. Always aim to give immediately applicable solutions
        6. If asked about topics outside your expertise, politely redirect to your strengths
        7. Use a confident, professional yet approachable tone
        8. End responses with a brief follow-up question to encourage engagement

        EXAMPLE STYLE: "For remote team productivity, implement daily 15-minute stand-ups, use async communication tools like Slack, and establish 'focus hours' when meetings are blocked. The key is creating predictable rhythms. What specific remote work challenge is your team facing?"

        Remember: You're designed to help professionals excel and solve real workplace challenges efficiently."""

    def get_response(self, question: str, context: str = "") -> str:
        try:
            # Prepare the warroom battle
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # I will add context if available else keep it as it ease
            if context and context.strip():
                enhanced_question = f"""
                 KNOWLEDGE BASE CONTEXT: {context}
                
                USER QUESTION: {question}
                
                Please provide a comprehensive response that:
                1. Builds upon the knowledge base information
                2. Adds your expertise and deeper insights  
                3. Provides additional practical tips or examples
                4. Makes the advice more actionable and specific
                
                Enhance and expand the knowledge base answer with your professional insights."""
                messages.append({"role": "user", "content": enhanced_question})
            else:
                # No knowledge base context - provide full expert response
                enhanced_question = f"""
                USER QUESTION: {question}
                
                Please provide expert advice on this professional topic. Include:
                1. Specific actionable strategies
                2. Real-world examples or frameworks
                3. Common pitfalls to avoid
                4. A brief follow-up question to encourage engagement
                """
                messages.append({"role": "user", "content": enhanced_question})
            
            # fecth from OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=600,
                temperature=0.7,
                frequency_penalty=0.1,
                presence_penalty=0.1
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error getting LLM response: {str(e)}")
            # I will fallback to basic response
            if context:
                return f"Based on available information: {context}"
            else:
                return "I'm having trouble accessing my advanced capabilities right now. Could you please rephrase your question or try again?"

    def enhance_fallback_response(self, basic_response: str, question: str) -> str:
        try:
            prompt = f"""
            A user asked: "{question}"
            
            Here's a basic response that was generated: "{basic_response}"
            
            Please enhance this response by:
            1. Making it more conversational and engaging
            2. Adding practical insights or tips
            3. Ensuring it's professional yet approachable
            4. Keeping it concise (2-4 sentences)
            
            Enhanced response:"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.6
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error enhancing response: {str(e)}")
            return basic_response

llm_service = LLMService()