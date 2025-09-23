import tkinter as tk
from tkinter import scrolledtext, messagebox
import re
import random
import sys
import os

try:
    import numpy as np
    TEM_NUMPY = True
except ImportError:
    TEM_NUMPY = False
    
    class VetorSimples:
        def __init__(self, dados):
            self.dados = dados
            
        def produto_escalar(self, outro):
            return sum(a * b for a, b in zip(self.dados, outro.dados))
            
        def norma(self):
            return sum(x * x for x in self.dados) ** 0.5

class ChatbotFoguetes:
    def __init__(self):
        self.conhecimento = self.carregar_conhecimento()
        self.palavras_chave = self.extrair_palavras_chave()
        
    def carregar_conhecimento(self):
        return [
            {
                'perguntas': [
                    'o que é cobruf', 'competição cobruf', 'sobre cobruf', 
                    'o que significa cobruf', 'defina cobruf', 'explique cobruf',
                    'me fale sobre a competição cobruf', 'o que é a competição cobruf'
                ],
                'resposta': '''A COBRUF (Competição Brasileira Universitária de Foguetes) é uma competição nacional onde equipes universitárias projetam, constroem e lançam foguetes experimentais. 

Detalhes importantes:
- Organizada pela UNIFOA
- Foco em foguetes de propulsão sólida
- Várias categorias por altitude e complexidade
- Avaliação leva em conta projeto, relatórios e desempenho no lançamento

É uma das principais competições do Brasil para estudantes de engenharia.'''
            },
            {
                'perguntas': [
                    'quais competições existem', 'competições brasileiras', 'outras competições',
                    'quais são as competições de foguete', 'competições universitárias',
                    'onde competir com foguetes', 'eventos de foguetes no brasil'
                ],
                'resposta': '''Principais competições no Brasil:

1. COBRUF - Competição Brasileira Universitária de Foguetes
2. LAAC - Latin American Aerospace Challenge  
3. Competição Regional Nordeste
4. Festival de Minifoguetes
5. Olimpíada Brasileira de Astronomia (categoria foguetes)

Tem também competições internacionais como Spaceport America Cup e IREC.'''
            },
            {
                'perguntas': ['como começar', 'iniciar projeto', 'primeiros passos', 'dicas para iniciantes'],
                'resposta': '''Dicas para começar:

1. **Estude a teoria**: Aerodinâmica, propulsão, estabilidade
2. **Use software**: Aprenda OpenRocket
3. **Comece simples**: Foguete de baixa altitude primeiro
4. **Materiais básicos**: PVC, aletas de madeira
5. **Motor comercial**: Use motores prontos no início
6. **Participe**: Eventos locais são ótimos para aprender

Recomendo começar com projetos de 1-2kg até 500m de altitude.'''
            }
        ]
    
    def extrair_palavras_chave(self):
        palavras_importantes = set()
        
        for topico in self.conhecimento:
            for pergunta in topico['perguntas']:
                palavras = self.limpar_texto(pergunta)
                palavras_importantes.update(palavras)
                
        return list(palavras_importantes)
    
    def limpar_texto(self, texto):
        texto = texto.lower().strip()
        texto = re.sub(r'[^\w\s]', '', texto)
        palavras = texto.split()
        
        palavras_vazias = {
            'o', 'a', 'os', 'as', 'um', 'uma', 'de', 'do', 'da', 'em', 'no', 'na',
            'por', 'para', 'com', 'sem', 'que', 'como', 'é', 'são', 'meu', 'minha'
        }
        
        return [palavra for palavra in palavras 
                if palavra not in palavras_vazias and len(palavra) > 2]
    
    def analisar_pergunta(self, texto_pergunta):
        palavras = self.limpar_texto(texto_pergunta)
        if not palavras:
            return self.vetor_vazio()
            
        frequencias = {}
        for palavra in palavras:
            frequencias[palavra] = frequencias.get(palavra, 0) + 1
        
        if TEM_NUMPY:
            vetor = np.zeros(len(self.palavras_chave))
            for i, palavra in enumerate(self.palavras_chave):
                if palavra in frequencias:
                    vetor[i] = frequencias[palavra] / len(palavras)
            return vetor
        else:
            vetor = [0.0] * len(self.palavras_chave)
            for i, palavra in enumerate(self.palavras_chave):
                if palavra in frequencias:
                    vetor[i] = frequencias[palavra] / len(palavras)
            return VetorSimples(vetor)
    
    def vetor_vazio(self):
        if TEM_NUMPY:
            return np.zeros(len(self.palavras_chave))
        else:
            return VetorSimples([0.0] * len(self.palavras_chave))
    
    def calcular_similaridade(self, vetor1, vetor2):
        if TEM_NUMPY:
            produto = np.dot(vetor1, vetor2)
            norma1 = np.linalg.norm(vetor1)
            norma2 = np.linalg.norm(vetor2)
        else:
            produto = vetor1.produto_escalar(vetor2)
            norma1 = vetor1.norma()
            norma2 = vetor2.norma()
        
        if norma1 == 0 or norma2 == 0:
            return 0
            
        return produto / (norma1 * norma2)
    
    def encontrar_resposta(self, pergunta):
        pergunta = pergunta.lower()
        
        for topico in self.conhecimento:
            for pergunta_base in topico['perguntas']:
                if pergunta_base in pergunta:
                    return topico['resposta']
        
        vetor_pergunta = self.analisar_pergunta(pergunta)
        melhor_score = 0
        melhor_resposta = None
        
        for topico in self.conhecimento:
            for pergunta_base in topico['perguntas']:
                vetor_base = self.analisar_pergunta(pergunta_base)
                score = self.calcular_similaridade(vetor_pergunta, vetor_base)
                
                if score > melhor_score:
                    melhor_score = score
                    melhor_resposta = topico['resposta']
        
        if melhor_score > 0.2:
            return melhor_resposta
        else:
            return self.resposta_generica(pergunta)
    
    def resposta_generica(self, pergunta):
        pergunta = pergunta.lower()
        
        if any(palavra in pergunta for palavra in ['oi', 'olá', 'hello', 'bom dia', 'boa tarde']):
            return "E aí! Sou especialista em foguetes experimentais da UFPE. Posso ajudar com projetos, competições, cálculos e segurança. Qual sua dúvida?"
        
        if any(palavra in pergunta for palavra in ['obrigado', 'valeu', 'agradeço', 'thanks']):
            return "Tamo junto! Boa sorte com seu projeto de foguetes! 🚀"
        
        if any(palavra in pergunta for palavra in ['tchau', 'bye', 'sair', 'até logo']):
            return "Falou! Se tiver mais dúvidas sobre foguetes, é só chamar!"
        
        opcoes = [
            "Interessante! Meu foco é foguetes experimentais universitários. Pode perguntar sobre COBRUF, projeto, motores ou segurança?",
            "Essa é específica. Posso ajudar mais com competições, cálculo de estabilidade, materiais ou sistemas de recuperação.",
            "Não manjo muito disso. Posso auxiliar com projeto de foguetes, competições como COBRUF, ou questões técnicas básicas.",
            "Sou mais focado em foguetes experimentais pra competições universitárias. Que tal perguntar sobre COBRUF, OpenRocket, ou projeto?",
        ]
        
        return random.choice(opcoes)

class InterfaceChat:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Chatbot Foguetes UFPE")
        self.janela.geometry("700x600")
        self.janela.configure(bg='#1a1a2e')
        
        self.janela.eval('tk::PlaceWindow . center')
        
        self.chatbot = ChatbotFoguetes()
        self.criar_interface()
        
    def criar_interface(self):
        cabecalho = tk.Frame(self.janela, bg='#16213e', height=80)
        cabecalho.pack(fill='x', padx=10, pady=5)
        cabecalho.pack_propagate(False)
        
        titulo = tk.Label(cabecalho, 
                         text="🤖 Chatbot - Foguetes Experimentais UFPE",
                         font=('Arial', 14, 'bold'),
                         fg='white',
                         bg='#16213e')
        titulo.pack(expand=True)
        
        subtitulo = tk.Label(cabecalho,
                           text="Engenharia Mecânica",
                           font=('Arial', 10),
                           fg='#e94560',
                           bg='#16213e')
        subtitulo.pack()
        
        area_conversa_frame = tk.Frame(self.janela, bg='#1a1a2e')
        area_conversa_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.historico = scrolledtext.ScrolledText(area_conversa_frame,
                                                  wrap=tk.WORD,
                                                  width=80,
                                                  height=20,
                                                  font=('Arial', 10),
                                                  bg='#0f3460',
                                                  fg='white',
                                                  insertbackground='white')
        self.historico.pack(fill='both', expand=True)
        self.historico.config(state='disabled')
        
        entrada_frame = tk.Frame(self.janela, bg='#1a1a2e')
        entrada_frame.pack(fill='x', padx=10, pady=10)
        
        lbl_instrucao = tk.Label(entrada_frame,
                                text="Digite sua pergunta:",
                                font=('Arial', 10, 'bold'),
                                fg='white',
                                bg='#1a1a2e')
        lbl_instrucao.pack(anchor='w')
        
        entrada_interna = tk.Frame(entrada_frame, bg='#1a1a2e')
        entrada_interna.pack(fill='x', pady=5)
        
        self.campo_pergunta = tk.Entry(entrada_interna,
                                      font=('Arial', 12),
                                      width=50,
                                      bg='#0f3460',
                                      fg='white',
                                      insertbackground='white')
        self.campo_pergunta.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.campo_pergunta.bind('<Return>', lambda e: self.enviar())
        
        btn_enviar = tk.Button(entrada_interna,
                              text="🚀 Enviar",
                              font=('Arial', 10, 'bold'),
                              bg='#e94560',
                              fg='white',
                              command=self.enviar,
                              width=10)
        btn_enviar.pack(side='right')
        
        exemplos_frame = tk.Frame(self.janela, bg='#1a1a2e')
        exemplos_frame.pack(fill='x', padx=10, pady=5)
        
        lbl_exemplos = tk.Label(exemplos_frame,
                               text="💡 Exemplos: 'Como calcular estabilidade?', 'Que materiais usar?', 'Me fala da COBRUF'",
                               font=('Arial', 9),
                               fg='#bdc3c7',
                               bg='#1a1a2e',
                               wraplength=650)
        lbl_exemplos.pack()
        
        self.mostrar_mensagem("Sistema", self.mensagem_inicial())
    
    def mensagem_inicial(self):
        return '''E aí, bem-vindo ao Chatbot de Foguetes Experimentais! 🚀

Sou especializado em ajudar estudantes da UFPE com projetos de foguetes pra competições como a COBRUF.

Posso ajudar com:
• 📊 Cálculos e projetos técnicos
• 🏆 Competições universitárias  
• 🔧 Componentes e materiais
• ⚠️ Normas de segurança
• 💻 Softwares de simulação

Manda sua pergunta que eu te ajudo!'''
    
    def mostrar_mensagem(self, quem, mensagem):
        self.historico.config(state='normal')
        
        if quem == "Sistema":
            cor = "#e94560"
            icone = "🤖 "
        elif quem == "Você":
            cor = "#3498db" 
            icone = "👤 "
        else:
            cor = "#2ecc71"
            icone = "🤖 "
        
        self.historico.insert(tk.END, f"{icone}{quem}:\n", f"cabecalho_{quem}")
        self.historico.tag_configure(f"cabecalho_{quem}", foreground=cor, font=('Arial', 10, 'bold'))
        
        self.historico.insert(tk.END, f"{mensagem}\n\n")
        
        self.historico.config(state='disabled')
        self.historico.see(tk.END)
    
    def enviar(self):
        pergunta = self.campo_pergunta.get().strip()
        
        if not pergunta:
            messagebox.showwarning("Aviso", "Digite alguma coisa aí!")
            return
        
        self.mostrar_mensagem("Você", pergunta)
        self.campo_pergunta.delete(0, tk.END)
        
        self.janela.after(100, self.processar, pergunta)
    
    def processar(self, pergunta):
        try:
            resposta = self.chatbot.encontrar_resposta(pergunta)
            self.mostrar_mensagem("Chatbot", resposta)
        except Exception as erro:
            mensagem_erro = f"Opa, deu um erro. Tenta de novo!\nErro: {str(erro)}"
            self.mostrar_mensagem("Sistema", mensagem_erro)

def main():
    try:
        janela = tk.Tk()
        app = InterfaceChat(janela)
        janela.mainloop()
    except Exception as e:
        print(f"Erro ao iniciar: {e}")
        input("Pressione Enter pra sair...")

if __name__ == "__main__":
    main()
