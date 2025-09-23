import tkinter as tk
from tkinter import scrolledtext, messagebox
import re
import numpy as np
from collections import Counter
import math
import random

class NLPChatbot:
    def __init__(self):
        self.base_conhecimento = self.carregar_base_conhecimento()
        self.vocabulario = self.construir_vocabulario()
        
    def carregar_base_conhecimento(self):
        return [
            {
                'perguntas': [
                    'o que é cobruf', 'competição cobruf', 'sobre cobruf', 
                    'o que significa cobruf', 'defina cobruf', 'explique cobruf',
                    'me fale sobre a competição cobruf', 'o que é a competição cobruf'
                ],
                'resposta': '''A COBRUF (Competição Brasileira Universitária de Foguetes) é uma competição nacional onde equipes universitárias projetam, constroem e lançam foguetes experimentais. 

Principais características:
- Organizada pela UNIFOA
- Foco em foguetes de propulsão sólida
- Categorias por altitude e complexidade
- Avaliação de projeto, relatórios e desempenho no lançamento

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

Internacionalmente existem também a Spaceport America Cup e a IREC.'''
            },
            {
                'perguntas': [
                    'como funciona o motor', 'propulsão do foguete', 'sistema de propulsão',
                    'combustível para foguetes', 'motor foguete experimental',
                    'como o motor funciona', 'propulsão sólida', 'químico do motor'
                ],
                'resposta': '''Os foguetes experimentais usam principalmente propulsão sólida:

Combustíveis comuns:
- KNSB (Nitrato de Potássio + Sorbitol)
- KNDX (Nitrato de Potássio + Dextrose)
- Outros compostos químicos específicos

Funcionamento:
1. Ignição do propelente
2. Combustão gera gases quentes
3. Gases expandem e saem pelo bocal
4. Reação empurra o foguete para cima

A queima é auto-sustentada até acabar o combustível.'''
            },
            {
                'perguntas': [
                    'materiais para construir', 'estrutura do foguete', 'fuselagem materiais',
                    'que material usar', 'construção do foguete', 'materiais leves',
                    'nariz do foguete material', 'aletas material'
                ],
                'resposta': '''Materiais recomendados para foguetes experimentais:

Estrutura principal:
- Fibra de vidro (mais comum)
- Fibra de carbono (alto desempenho)
- PVC (para protótipos e testes)
- Alumínio (componentes estruturais)

Aletas:
- Madeira (balsa ou compensado)
- Acrílico
- Fibra de vidro

Nariz:
- Plástico usinado
- Madeira torneada
- Impressão 3D'''
            },
            {
                'perguntas': [
                    'sistema de recuperação', 'paraquedas como funciona', 'recuperar foguete',
                    'ejeção do paraquedas', 'como o paraquedas abre', 'sistema de ejeção',
                    'recuperação após lançamento'
                ],
                'resposta': '''Sistema de recuperação típico:

1. **Ativação**: No apogeu (ponto mais alto) ou por timer
2. **Ejeção**: Carga pirotécnica ou mola empurra o paraquedas
3. **Abertura**: Paraquedas se infla e reduz a velocidade
4. **Queda**: Foguete desce lentamente para recuperação

Componentes:
- Paraquedas principal e de reserva
- Sistema de ejeção (black powder, CO2)
- Altímetro eletrônico
- Swivel para evitar torção'''
            },
            {
                'perguntas': [
                    'como calcular estabilidade', 'estabilidade do foguete', 'centro de gravidade',
                    'centro de pressão', 'como tornar estável', 'calcular cp cg',
                    'aletas tamanho', 'estabilidade aerodinâmica'
                ],
                'resposta': '''Cálculo de estabilidade:

**Regra fundamental**: CG (Centro de Gravidade) deve estar à frente do CP (Centro de Pressão)

Métodos:
1. **Regra dos calibres**: CP deve estar 1-2 calibres atrás do CG
2. **Software**: OpenRocket, Rocksim calculam automaticamente
3. **Teste de giro**: Verificação prática antes do lançamento

Fórmula básica: Margem de estabilidade = (Distância CG-CP) / Diâmetro do foguete
Ideal: 1.5 a 2.0 calibres'''
            },
            {
                'perguntas': [
                    'software para projeto', 'openrocket como usar', 'simular foguete',
                    'ferramentas de projeto', 'programas para foguetes',
                    'simulação trajetória', 'software simulação'
                ],
                'resposta': '''Softwares mais usados:

1. **OpenRocket** (Gratuito) - Completo para projeto e simulação
2. **Rocksim** (Pago) - Profissional, muito preciso
3. **RASAero** - Foco em aerodinâmica
4. **Excel** - Cálculos personalizados

OpenRocket é o mais recomendado para iniciantes:
- Interface amigável
- Simula trajetória, altitude, velocidade
- Calcula estabilidade automaticamente
- Biblioteca de motores e materiais'''
            },
            {
                'perguntas': [
                    'normas de segurança', 'procedimentos seguros', 'segurança lançamento',
                    'epi para foguetes', 'precauções segurança', 'protocolos segurança',
                    'como lançar com segurança'
                ],
                'resposta': '''Normas de segurança essenciais:

**EPI Obrigatório**:
- Óculos de proteção
- Capacete
- Roupas não inflamáveis

**Procedimentos**:
- Área de lançamento isolada
- Distância mínima de segurança
- Extintor disponível
- Checklist pré-lançamento
- Comunicação clara entre equipe

**Manuseio propelentes**:
- Em área ventilada
- Com equipamento adequado
- Seguindo protocolos específicos'''
            },
            {
                'perguntas': [
                    'equipe ufpe', 'foguetes ufpe', 'projeto ufpe',
                    'ufpe competições', 'engenharia mecânica ufpe foguetes',
                    'grupo foguetes ufpe', 'ufpe cobruf'
                ],
                'resposta': '''A UFPE tem tradição em foguetes experimentais!

**Como participar**:
- Contate o departamento de Engenharia Mecânica
- Procure por grupos de extensão
- Participe de disciplinas relacionadas a aeroespacial
- Entre em contato com o Centro de Tecnologia

**Histórico**:
A UFPE já participou de várias edições da COBRUF com bons resultados.'''
            },
            {
                'perguntas': [
                    'como começar', 'iniciar projeto', 'primeiros passos',
                    'dicas para iniciantes', 'começar foguete experimental',
                    'projeto primeiro foguete', 'iniciante dicas'
                ],
                'resposta': '''Passos para iniciar:

1. **Estudo teórico**: Aerodinâmica, propulsão, estabilidade
2. **Software**: Aprenda OpenRocket
3. **Projeto simples**: Comece com foguete de baixa altitude
4. **Materiais básicos**: PVC, aletas de madeira
5. **Motor comercial**: Use motores prontos inicialmente
6. **Competições**: Participe de eventos locais

Recomendo começar com projetos de 1-2kg e altitude até 500m.'''
            }
        ]
    
    def construir_vocabulario(self):
        vocabulario = set()
        for item in self.base_conhecimento:
            for pergunta in item['perguntas']:
                palavras = self.preprocessar_texto(pergunta)
                vocabulario.update(palavras)
        return list(vocabulario)
    
    def preprocessar_texto(self, texto):
        texto = texto.lower()
        texto = re.sub(r'[^\w\s]', '', texto)
        palavras = texto.split()
        
        stopwords = {'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas', 
                    'de', 'do', 'da', 'dos', 'das', 'em', 'no', 'na', 
                    'nos', 'nas', 'por', 'para', 'com', 'sem', 'sob',
                    'sobre', 'entre', 'que', 'como', 'é', 'são', 'seu',
                    'sua', 'seus', 'suas', 'meu', 'minha', 'meus', 'minhas'}
        
        return [palavra for palavra in palavras if palavra not in stopwords and len(palavra) > 2]
    
    def calcular_tfidf(self, texto):
        palavras = self.preprocessar_texto(texto)
        tf = Counter(palavras)
        
        vetor_tf = np.zeros(len(self.vocabulario))
        for i, palavra in enumerate(self.vocabulario):
            if palavra in tf:
                vetor_tf[i] = tf[palavra] / len(palavras)
        
        vetor_idf = np.ones(len(self.vocabulario))
        
        return vetor_tf * vetor_idf
    
    def similaridade_cosseno(self, vetor1, vetor2):
        dot_product = np.dot(vetor1, vetor2)
        norm1 = np.linalg.norm(vetor1)
        norm2 = np.linalg.norm(vetor2)
        
        if norm1 == 0 or norm2 == 0:
            return 0
        return dot_product / (norm1 * norm2)
    
    def processar_pergunta_nlp(self, pergunta):
        vetor_pergunta = self.calcular_tfidf(pergunta)
        
        melhor_similaridade = 0
        melhor_resposta = None
        
        for item in self.base_conhecimento:
            for pergunta_base in item['perguntas']:
                vetor_base = self.calcular_tfidf(pergunta_base)
                similaridade = self.similaridade_cosseno(vetor_pergunta, vetor_base)
                
                if similaridade > melhor_similaridade:
                    melhor_similaridade = similaridade
                    melhor_resposta = item['resposta']
        
        if melhor_similaridade > 0.3:
            return melhor_resposta
        else:
            return self.gerar_resposta_padrao(pergunta)
    
    def gerar_resposta_padrao(self, pergunta):
        pergunta = pergunta.lower()
        
        if any(palavra in pergunta for palavra in ['oi', 'olá', 'hello', 'bom dia', 'boa tarde', 'boa noite']):
            return "Olá! Sou especialista em foguetes experimentais da UFPE. Posso ajudar com projetos, competições, cálculos e segurança. Como posso ajudá-lo?"
        
        if any(palavra in pergunta for palavra in ['obrigado', 'valeu', 'agradeço', 'thanks']):
            return "De nada! Fico feliz em ajudar. Boa sorte com seu projeto de foguetes! 🚀"
        
        if any(palavra in pergunta for palavra in ['tchau', 'bye', 'sair', 'até logo']):
            return "Até logo! Se tiver mais dúvidas sobre foguetes experimentais, estarei aqui!"
        
        respostas_padrao = [
            "Interessante sua pergunta! Minha especialidade é foguetes experimentais universitários. Pode me perguntar sobre COBRUF, projeto, motores ou segurança?",
            "Essa é uma questão específica. Posso ajudar melhor com tópicos como competições, cálculo de estabilidade, materiais ou sistemas de recuperação de foguetes.",
            "Não tenho informações detalhadas sobre isso no momento. Posso auxiliar com: projeto de foguetes, competições como COBRUF, ou questões técnicas básicas.",
            "Sou focado em foguetes experimentais para competições universitárias. Que tal perguntar sobre COBRUF, OpenRocket, ou projeto de foguetes?"
        ]
        
        return random.choice(respostas_padrao)

class InterfaceChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot NLP - Foguetes Experimentais UFPE")
        self.root.geometry("700x600")
        self.root.configure(bg='#1a1a2e')
        
        self.chatbot = NLPChatbot()
        self.criar_interface()
        
    def criar_interface(self):
        header_frame = tk.Frame(self.root, bg='#16213e', height=80)
        header_frame.pack(fill='x', padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        titulo = tk.Label(header_frame, 
                         text="🤖 Chatbot Inteligente - Foguetes Experimentais UFPE",
                         font=('Arial', 14, 'bold'),
                         fg='white',
                         bg='#16213e')
        titulo.pack(expand=True)
        
        subtitulo = tk.Label(header_frame,
                           text="Engenharia Mecânica",
                           font=('Arial', 10),
                           fg='#e94560',
                           bg='#16213e')
        subtitulo.pack()
        
        chat_frame = tk.Frame(self.root, bg='#1a1a2e')
        chat_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.area_chat = scrolledtext.ScrolledText(chat_frame,
                                                  wrap=tk.WORD,
                                                  width=80,
                                                  height=20,
                                                  font=('Arial', 10),
                                                  bg='#0f3460',
                                                  fg='white',
                                                  insertbackground='white')
        self.area_chat.pack(fill='both', expand=True)
        self.area_chat.config(state='disabled')
        
        entrada_frame = tk.Frame(self.root, bg='#1a1a2e')
        entrada_frame.pack(fill='x', padx=10, pady=10)
        
        lbl_instrucao = tk.Label(entrada_frame,
                                text="Digite sua pergunta:",
                                font=('Arial', 10, 'bold'),
                                fg='white',
                                bg='#1a1a2e')
        lbl_instrucao.pack(anchor='w')
        
        entrada_subframe = tk.Frame(entrada_frame, bg='#1a1a2e')
        entrada_subframe.pack(fill='x', pady=5)
        
        self.entrada_pergunta = tk.Entry(entrada_subframe,
                                        font=('Arial', 12),
                                        width=50,
                                        bg='#0f3460',
                                        fg='white',
                                        insertbackground='white')
        self.entrada_pergunta.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.entrada_pergunta.bind('<Return>', lambda e: self.enviar_pergunta())
        
        btn_enviar = tk.Button(entrada_subframe,
                              text="🚀 Enviar",
                              font=('Arial', 10, 'bold'),
                              bg='#e94560',
                              fg='white',
                              command=self.enviar_pergunta,
                              width=10)
        btn_enviar.pack(side='right')
        
        exemplos_frame = tk.Frame(self.root, bg='#1a1a2e')
        exemplos_frame.pack(fill='x', padx=10, pady=5)
        
        lbl_exemplos = tk.Label(exemplos_frame,
                               text="💡 Exemplos: 'Como calcular a estabilidade do meu foguete?', 'Que materiais usar na estrutura?', 'Me explique sobre a COBRUF'",
                               font=('Arial', 9),
                               fg='#bdc3c7',
                               bg='#1a1a2e',
                               wraplength=650)
        lbl_exemplos.pack()
        
        self.adicionar_mensagem("Sistema", self.mensagem_boas_vindas())
    
    def mensagem_boas_vindas(self):
        return '''Bem-vindo ao Chatbot Inteligente de Foguetes Experimentais! 🚀

Sou especializado em ajudar estudantes da UFPE com projetos de foguetes para competições como COBRUF.

Posso ajudar com:
• 📊 Cálculos e projetos técnicos
• 🏆 Competições universitárias
• 🔧 Componentes e materiais
• ⚠️ Normas de segurança
• 💻 Softwares de simulação

Digite sua pergunta em linguagem natural - eu entenderei!'''
    
    def adicionar_mensagem(self, remetente, mensagem):
        self.area_chat.config(state='normal')
        
        if remetente == "Sistema":
            cor = "#e94560"
            prefixo = "🤖 "
        elif remetente == "Você":
            cor = "#3498db"
            prefixo = "👤 "
        else:
            cor = "#2ecc71"
            prefixo = "🤖 "
        
        self.area_chat.insert(tk.END, f"{prefixo}{remetente}:\n", f"header_{remetente}")
        self.area_chat.tag_configure(f"header_{remetente}", foreground=cor, font=('Arial', 10, 'bold'))
        
        self.area_chat.insert(tk.END, f"{mensagem}\n\n")
        
        self.area_chat.config(state='disabled')
        self.area_chat.see(tk.END)
    
    def enviar_pergunta(self):
        pergunta = self.entrada_pergunta.get().strip()
        
        if not pergunta:
            messagebox.showwarning("Aviso", "Por favor, digite uma pergunta.")
            return
        
        self.adicionar_mensagem("Você", pergunta)
        self.entrada_pergunta.delete(0, tk.END)
        
        self.root.after(100, self.processar_resposta, pergunta)
    
    def processar_resposta(self, pergunta):
        try:
            resposta = self.chatbot.processar_pergunta_nlp(pergunta)
            self.adicionar_mensagem("Chatbot", resposta)
        except Exception as e:
            self.adicionar_mensagem("Sistema", f"Erro no processamento: {str(e)}")

def main():
    root = tk.Tk()
    app = InterfaceChatbot(root)
    root.mainloop()

if __name__ == "__main__":
    main()