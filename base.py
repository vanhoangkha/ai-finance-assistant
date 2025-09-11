import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import random

icons = {
    "assistant": "🤖",
    "user": "👤",
}

particles_js = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Particles.js</title>
  <style>
  #particles-js {
    position: fixed;
    width: 100vw;
    height: 100vh;
    top: 0;
    left: 0;
    z-index: -1; /* Send the animation to the back */
  }
  .content {
    position: relative;
    z-index: 1;
    color: white;
  }
  
</style>
</head>
<body>
  <div id="particles-js"></div>
  <div class="content">
    <!-- Placeholder for Streamlit content -->
  </div>
  <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
  <script>
    particlesJS("particles-js", {
      "particles": {
        "number": {
          "value": 300,
          "density": {
            "enable": true,
            "value_area": 800
          }
        },
        "color": {
          "value": "#000000"
        },
        "shape": {
          "type": "circle",
          "stroke": {
            "width": 0,
            "color": "#ffffff"
          },
          "polygon": {
            "nb_sides": 5
          },
          "image": {
            "src": "",
            "width": 100,
            "height": 100
          }
        },
        "opacity": {
          "value": 0.5,
          "random": false,
          "anim": {
            "enable": false,
            "speed": 1,
            "opacity_min": 0.2,
            "sync": false
          }
        },
        "size": {
          "value": 2,
          "random": true,
          "anim": {
            "enable": false,
            "speed": 40,
            "size_min": 0.1,
            "sync": false
          }
        },
        "line_linked": {
          "enable": true,
          "distance": 100,
          "color": "#000000",
          "opacity": 0.22,
          "width": 1
        },
        "move": {
          "enable": true,
          "speed": 0.2,
          "direction": "none",
          "random": false,
          "straight": false,
          "out_mode": "out",
          "bounce": true,
          "attract": {
            "enable": false,
            "rotateX": 600,
            "rotateY": 1200
          }
        }
      },
      "interactivity": {
        "detect_on": "canvas",
        "events": {
          "onhover": {
            "enable": true,
            "mode": "grab"
          },
          "onclick": {
            "enable": true,
            "mode": "repulse"
          },
          "resize": true
        },
        "modes": {
          "grab": {
            "distance": 100,
            "line_linked": {
              "opacity": 1
            }
          },
          "bubble": {
            "distance": 400,
            "size": 2,
            "duration": 2,
            "opacity": 0.5,
            "speed": 1
          },
          "repulse": {
            "distance": 200,
            "duration": 0.4
          },
          "push": {
            "particles_nb": 2
          },
          "remove": {
            "particles_nb": 3
          }
        }
      },
      "retina_detect": true
    });
  </script>
</body>
</html>
"""
welcome_messages = [
    "Hello! I'm Finance Chatbot, your AI assistant for financial analysis. Ask me anything!",
    "Hi! I'm Finance Chatbot, your AI guide for financial data. How can I help you?",
    "Hey! I'm Finance Chatbot, your AI investment advisor. What would you like to explore?",
    "Hello! I'm Finance Chatbot, your AI tool for understanding financial markets. How can I assist?",
    "Hi there! I'm Finance Chatbot, your AI stock analysis tool. What do you need?",
    "Hello! I'm Finance Chatbot, your AI assistant for easy financial data understanding. How can I help?",
    "Welcome! I'm Finance Chatbot, your smart AI market analysis tool. How can I support you?",
    "Hello! I'm Finance Chatbot, your AI investment guide. Ask me anything!",
    "Hi! I'm Finance Chatbot, your smart AI financial analysis assistant. What would you like to explore?",
    "Hey! I'm Finance Chatbot, your AI market analysis assistant. How can I help today?",
]

message = random.choice(welcome_messages)

system_prompt = """
You are Finance Chatbot, an expert AI financial advisor specializing in stock market analysis and investment guidance. Current date: September 2024.

CORE EXPERTISE:
- Advanced technical & fundamental analysis
- Real-time market insights & trend identification  
- Risk assessment & portfolio optimization
- Trading strategies for all experience levels

RESPONSE FRAMEWORK:
1. ANALYZE: Assess user's question context and intent
2. PROVIDE: Clear, actionable insights with supporting data
3. EXPLAIN: Break down complex concepts into digestible parts
4. RECOMMEND: Specific next steps or strategies when appropriate

COMMUNICATION STYLE:
- Professional yet approachable tone
- Use bullet points for clarity
- Include relevant examples and analogies
- Acknowledge uncertainty when data is incomplete
- Always emphasize risk management

SPECIALIZATIONS:
- Stock screening & valuation
- Technical indicator interpretation
- Market sentiment analysis
- Economic event impact assessment
- Portfolio diversification strategies

Remember: All advice is educational. Users should conduct their own research and consider their risk tolerance before making investment decisions.
"""

def init_home_state(_message): 
  if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": message}]
  if "exif_df" not in st.session_state:
      st.session_state["exif_df"] = pd.DataFrame()
  if "url_exif_df" not in st.session_state:
      st.session_state["url_exif_df"] = pd.DataFrame()
  if "show_expanders" not in st.session_state:
      st.session_state.show_expanders = True
  if "reset_trigger" not in st.session_state:
      st.session_state.reset_trigger = False
  if "image_url" not in st.session_state:
      st.session_state["image_url"] = ""
  if "follow_up" not in st.session_state:
      st.session_state.follow_up = False
  if "show_animation" not in st.session_state:
      st.session_state.show_animation = True


def init_stock_advisor(): 
  if "messages" not in st.session_state:
      st.session_state["messages"] = [{"role": "assistant", "content": message}]
  if 'generated' not in st.session_state:
      st.session_state['generated'] = []
  if 'past' not in st.session_state:
      st.session_state['past'] = []
  if 'model_name' not in st.session_state:
      st.session_state['model_name'] = []
  if 'cost' not in st.session_state:
      st.session_state['cost'] = []
  if 'total_tokens' not in st.session_state:
      st.session_state['total_tokens'] = []
  if 'total_cost' not in st.session_state:
      st.session_state['total_cost'] = 0.0

def init_slidebar():
  with st.sidebar:
      st.markdown(
          f"""
          <div style='display: flex; align-items: center;'>
              <h1 style='margin: 0;'>Finance Chatbot</h1>
          </div>
          """,
          unsafe_allow_html=True,
      )

      st.markdown(
          """
          <style>
              [data-testid="stSidebarNav"]::before {
                  content: "Finance Chatbot";
                  margin-left: 20px;
                  font-size: 20px;
                  position: relative;
              }
          </style>
          """,
          unsafe_allow_html=True,
      )
      
      st.sidebar.button(
          "🗑 Clear Chat History",
          on_click=clear_chat_history,
          key="sidebar_clear_chat_history",
      )

def init_animation():
  if 'reset_trigger' not in st.session_state:
    st.session_state.reset_trigger = False
  if st.session_state.reset_trigger:
      unique_key = "chat_input_" + str(hash("Snowflake Arctic is cool"))
      st.session_state.show_animation = False
      
  if "has_snowed" not in st.session_state:
      st.snow()
      st.session_state["has_snowed"] = True

  if 'show_animation' not in st.session_state:
    st.session_state.show_animation = False

  if st.session_state.show_animation:
      components.html(particles_js, height=370, scrolling=False)

def init_dialog():
  for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=icons[message["role"]]):
        st.write(message["content"])
        if message == st.session_state["messages"][0]:
            if st.button("About Finance Chatbot?"):
                st.info("Finance Chatbot is your AI-powered assistant for financial analysis, market insights, and investment guidance. Ask me anything about stocks, markets, or financial planning!")
                
                
def right_message(st, message):
    st.markdown(
        f"""
        <div style="display: flex; justify-content: flex-end; align-items: center; margin-bottom: 10px;">
            <div style="text-align: right;">
                {message}
            </div>
            <span style="font-size: 40px; margin-left: 10px;">👤</span>
        </div>
        """,
        unsafe_allow_html=True
    )

def clear_chat_history():
    st.session_state.reset_trigger = not st.session_state.reset_trigger
    st.session_state.show_expanders = True
    st.session_state.show_animation = True
    st.session_state.messages = [{"role": "assistant", "content": message}]
    st.session_state["exif_df"] = pd.DataFrame()
    st.session_state["url_exif_df"] = pd.DataFrame()
    st.cache_data.clear()
    st.success("Chat History Cleared!")

def clear_stock_advisor():
    st.session_state.show_animation = True
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state.messages = [{"role": "assistant", "content": message}]
    st.session_state['number_tokens'] = []
    st.session_state['model_name'] = []
    st.session_state['cost'] = []
    st.session_state['total_cost'] = 0.0
    st.session_state['total_tokens'] = []
    #counter_placeholder.write(f"Total cost of this conversation: $${st.session_state['total_cost']:.5f}")

def show_video(video_url):
    st.video(video_url, loop=False, autoplay=True, muted=False)


def get_num_tokens(prompt):
    try:
        # Simple token estimation: roughly 4 characters per token
        return len(prompt) // 4
    except Exception:
        return 0


