# response_model.py

import random
from datetime import datetime
import re

class ResponseModel:
    def __init__(self):
        self.conversation_history = {}
        self.session_counts = {}
        
        # Comprehensive pattern dictionary with expanded responses
        self.patterns = {
            'anxiety': {
                'patterns': [
                    r'anxi(ous|ety)', r'worried?', r'stress(ed|ful)', 
                    r'nervous', r'panic', r'overwhelm(ed|ing)',
                    r'fear(ed|ful)?', r'scared', r'tense', r'uneasy',
                    r'restless', r'overthinking', r'cant\s+stop\s+thinking'
                ],
                'responses': [
                    "I notice you're feeling anxious. What brought these feelings up?",
                    "Anxiety can feel overwhelming. Would you like to explore what's causing these feelings?",
                    "When did you start feeling this anxiety? I'm here to listen without judgment.",
                    "It sounds like anxiety is really present for you. What would help you feel more grounded?",
                    "Sometimes anxiety can be intense. What specific worries are on your mind?",
                    "Would you like to try some breathing exercises to help with the anxiety?",
                    "I hear that anxiety is affecting you. How is it showing up in your daily life?",
                    "Anxiety often comes with physical sensations. What are you experiencing?",
                    "It's okay to feel anxious. Can we break down what's contributing to these feelings?",
                    "Let's explore these anxious thoughts together. What's weighing most heavily?",
                    "Anxiety can make us feel isolated. What support would be most helpful right now?",
                    "Would you like to try grounding yourself in the present moment?",
                    "Sometimes anxiety tells us stories about the future. What thoughts keep coming up?",
                    "I'm hearing how challenging this is. What feels most overwhelming?",
                    "Anxiety can affect our whole body. How is it manifesting for you?",
                    "Let's take it one step at a time. What's your biggest concern right now?",
                    "Would you like to explore some coping strategies for managing anxiety?",
                    "Anxiety can make everything feel urgent. What needs our attention first?",
                    "I'm here to support you through this. How can I help most effectively?",
                    "Sometimes anxiety needs to be heard. What do you think it's trying to tell you?",
                    "Your feelings are valid. Would you like to explore what triggers them?",
                    "Anxiety can make us feel out of control. What helps you feel more centered?",
                    "Let's understand your anxiety better. Have you noticed any patterns?",
                    "Would you like to try a relaxation technique together?",
                    "Anxiety often affects our breathing. Should we try some breathing exercises?",
                    "It's brave to talk about anxiety. How long has this been going on?",
                    "Sometimes anxiety protects us. What might it be protecting you from?",
                    "Would you like to break down these feelings into smaller pieces?",
                    "Anxiety can affect our relationships. How is it impacting yours?",
                    "Let's explore what makes the anxiety better or worse."
                ]
            },
            'depression': {
                'patterns': [
                    r'depress(ed|ion)', r'sad', r'down', r'hopeless',
                    r'unmotivated', r'tired', r'lonely', r'empty',
                    r'worthless', r'numb', r'exhausted', r'cant\s+cope'
                ],
                'responses': [
                    "I hear how difficult things are. Would you like to talk about what's happening?",
                    "Depression can feel really heavy. How long have you been carrying this?",
                    "It takes courage to share these feelings. What support would be most helpful?",
                    "I hear the pain in your words. What would a moment of relief look like?",
                    "Sometimes depression makes everything harder. What's been most challenging?",
                    "You don't have to carry this alone. How can I support you?",
                    "Depression can feel overwhelming. What would help right now?",
                    "I notice a lot of sadness in your words. Would you like to explore that?",
                    "It's okay to not be okay. How are you managing day to day?",
                    "Depression can affect our whole world. What changes have you noticed?",
                    "Would you like to talk about what might have triggered these feelings?",
                    "Sometimes depression lies to us about our worth. What has it been telling you?",
                    "Your feelings are valid. What would help you feel more supported?",
                    "Depression can make us feel very alone. What helps you feel connected?",
                    "Let's take things one step at a time. What feels manageable today?",
                    "I hear how overwhelming this is. What used to bring you joy?",
                    "Sometimes small steps help. What tiny thing could we focus on?",
                    "Depression can cloud our view of the future. How can we focus on today?",
                    "Would you like to explore some gentle ways to care for yourself?",
                    "It's okay to need help. What kind of support are you looking for?",
                    "Depression can affect our energy levels. How is it affecting yours?",
                    "Sometimes depression comes in waves. Where are you in that wave right now?",
                    "Your experience matters. What else would you like to share?",
                    "Depression can make us forget our strengths. What strengths have helped you cope?",
                    "Let's focus on what feels possible today. What's one small thing?",
                    "Would you like to talk about what support systems you have?",
                    "Depression can affect our sleep and appetite. Have you noticed changes?",
                    "It's important to be gentle with yourself. What would that look like today?",
                    "Sometimes depression needs to be witnessed. I'm here to listen.",
                    "Let's explore what might bring even a moment of peace."
                ]
            },
            'anger': {
                'patterns': [
                    r'angry?', r'mad', r'frustrat(ed|ing)', 
                    r'irritat(ed|ing)', r'upset', r'furious',
                    r'rage', r'hate', r'annoyed', r'fed up'
                ],
                'responses': [
                    "I can hear your anger. What triggered these feelings?",
                    "It's okay to feel angry. Would you like to talk about what happened?",
                    "Anger often tells us something important. What do you think it's saying?",
                    "Your anger is valid. What would help you feel heard?",
                    "Sometimes anger protects us. What might it be protecting you from?",
                    "I hear how frustrated you are. What needs to change?",
                    "Anger can be intense. How can I support you right now?",
                    "Would you like to explore what's beneath the anger?",
                    "It sounds like something really bothered you. Can you tell me more?",
                    "Anger can be a signal. What do you think it's signaling?",
                    "I'm hearing how upset you are. What would help in this moment?",
                    "Sometimes anger builds up over time. How long have you been feeling this way?",
                    "Your feelings are valid. What would make the situation better?",
                    "Anger can be overwhelming. Would you like to try some calming techniques?",
                    "I hear your frustration. What feels most unfair?",
                    "Let's explore these feelings. What's at the core of your anger?",
                    "Sometimes anger masks other emotions. What else might you be feeling?",
                    "Would you like to talk about healthy ways to express your anger?",
                    "Anger often comes with physical sensations. What are you noticing in your body?",
                    "It's okay to feel angry about things that matter to you. What matters here?",
                    "I'm here to listen without judgment. What else would you like to share?",
                    "Sometimes anger points to our boundaries. Have any been crossed?",
                    "Your anger deserves to be heard. What would you like to express?",
                    "Let's explore what triggered these feelings. What happened first?",
                    "Anger can be energizing. How would you like to channel this energy?",
                    "Would you like to try some grounding exercises to help manage the intensity?",
                    "I hear how important this is to you. What needs aren't being met?",
                    "Sometimes anger helps us identify our values. What values feel challenged?",
                    "Your reactions make sense. How can we address this situation?",
                    "Let's work through this together. What would resolution look like?"
                ]
            }
        }

        # Add follow-ups for deeper conversation
        self.follow_ups = [
            "How long have you been feeling this way?",
            "What do you think triggered these feelings?",
            "Have you noticed any patterns in when this happens?",
            "What would help you feel better right now?",
            "How has this been affecting your daily life?",
            "Would you like to explore some coping strategies together?",
            "What support would be most helpful?",
            "Have you talked to anyone else about this?",
            "What changes have you noticed in yourself?",
            "How do these feelings affect your relationships?",
            "What helps you cope when things get difficult?",
            "Would you like to try some relaxation techniques?",
            "What would feeling better look like for you?",
            "How can I best support you right now?",
            "What usually helps in situations like this?"
        ]

        # Professional referral messages
        self.referral_messages = [
            {
                'message': "I've really valued our conversation. Would you like to connect with a mental health professional who can provide more specialized support?",
                'contact': "AASRA provides 24/7 support at 91-9820466726."
            },
            {
                'message': "While I'm here to listen, a therapist could offer additional strategies and support. Would you like some recommendations?",
                'contact': "The Mind Wellness Clinic (1860-2662-345) offers professional counseling services."
            },
            {
                'message': "You've shown courage in sharing these feelings. Would you like to explore professional support options?",
                'contact': "Vandrevala Foundation (1860-2662-345) provides 24/7 mental health support."
            }
        ]

    def get_response(self, user_input, session_id):
        if session_id not in self.session_counts:
            self.session_counts[session_id] = 1
            self.conversation_history[session_id] = []
            return random.choice([
                "Hi! I'm here to listen and support you. How are you feeling today?",
                "Welcome! This is a safe space to talk. How are you doing?",
                "Hello! Thank you for reaching out. Would you like to share what's on your mind?",
                "Hi there! I'm here to support you. How are you feeling right now?"
            ])

        self.session_counts[session_id] += 1

        # Detect emotion and generate response
        emotion = self._detect_emotion(user_input.lower())
        response = self._generate_response(emotion, session_id)

        # Add to conversation history
        self.conversation_history[session_id].append({
            'user_input': user_input,
            'emotion': emotion,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })

        # Add professional referral after 6-7 messages
        if 6 <= self.session_counts[session_id] <= 8 and random.random() < 0.3:
            referral = random.choice(self.referral_messages)
            response = f"{response}\n\n{referral['message']}\n{referral['contact']}"

        return response

    def _detect_emotion(self, text):
        for emotion, data in self.patterns.items():
            for pattern in data['patterns']:
                if re.search(pattern, text):
                    return emotion
        return 'general'

    def _generate_response(self, emotion, session_id):
        responses = self.patterns.get(emotion, {'responses': [
            "I'm here to listen. Would you like to tell me more?",
            "How are you feeling about that?",
            "Would you like to explore this further?",
            "What's on your mind?",
            "I'm here to support you. What would you like to talk about?"
        ]})['responses']

        base_response = random.choice(responses)
        
        # Add follow-up 50% of the time
        if random.random() < 0.5:
            base_response = f"{base_response} {random.choice(self.follow_ups)}"

        return base_response

    def _is_crisis(self, text):
        crisis_keywords = ['suicide', 'kill myself', 'end it all', 'die', 'hurt myself']
        return any(keyword in text.lower() for keyword in crisis_keywords)