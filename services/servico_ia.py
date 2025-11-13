import json
import streamlit as st
from openai import OpenAI
from typing import Dict, Any
from openai import APIError, APIConnectionError

try:
    cliente = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("Erro ao inicializar o cliente OpenAI: A chave 'OPENAI_API_KEY' não está configurada em st.secrets.")
    cliente = None

def processar_solicitacao_ia(endereco_completo: str, descricao_usuario: str) -> Dict[str, Any]:
    if cliente is None:
        return {
            "erro": "Serviço de IA não inicializado. Verifique sua chave de API.",
            "endereco_consolidado": endereco_completo,
            "gravidade": "Indefinida",
            "servicos_acessados": [],
            "descricao_consolidada": descricao_usuario
        }
    
    json_esperado = {
        "type": "object",
        "properties": {
            "endereco_consolidado": {
                "type": "string",
                "description": "Versão resumida e limpa do endereço fornecido."
            },
            "gravidade": {
                "type": "string",
                "description": "O nível de gravidade da emergência. Deve ser um destes valores: 'Baixa', 'Média', 'Alta', 'Crítica'."
            },
            "servicos_acessados": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Lista de serviços de emergência necessários. Deve ser um subconjunto de: 'Bombeiros', 'SAMU', 'Polícia'."
            },
            "descricao_consolidada": {
                "type": "string",
                "description": "Resumo objetivo e profissional da ocorrência para uso em despacho."
            }
        },
        "required": ["endereco_consolidado", "gravidade", "servicos_acessados", "descricao_consolidada"]
    }

    contexto_sistema = f"""
    Você é um Analista de Emergências sênior. Sua tarefa é analisar o ENDEREÇO COMPLETO e a DESCRIÇÃO DO USUÁRIO.

    1. Consolide o endereço em um formato mais curto e direto, não coloque o País, porém mantenha o CEP, se houver informações a nível de construção mantenha elas.

    2. Classifique a gravidade da situação de acordo com o risco imediato à vida, usando APENAS UMA das opções: 'Baixa', 'Média', 'Alta' ou 'Crítica'.
    - **Baixa:** situações sem risco de morte ou ferimentos graves, como pequenos mal-estares seguidos de alguma melhora, desmaios leves, quedas sem lesão, incêndios controlados, barulhos, brigas verbais ou pedidos de ajuda preventiva.
    - **Média:** situações que podem se agravar, mas sem risco iminente de morte, como pessoa consciente com dor forte, princípio de incêndio, acidente leve com ferimentos moderados, ou mal-estar persistente.
    - **Alta:** risco evidente de morte se não houver atendimento rápido, como pessoa inconsciente, sangramento intenso, incêndio ativo, afogamento ou agressão física grave.
    - **Crítica:** risco imediato de morte ou grande número de vítimas, como parada cardiorrespiratória, desabamento, incêndio em grande proporção, múltiplos feridos, explosão ou tiroteio ativo.
    Importante: se a pessoa está consciente, falando normalmente e o ferimento é superficial (como corte pequeno, torção leve ou sangramento controlado), classifique como Baixa — mesmo que haja dor ou dificuldade de locomoção.
    Só classifique como Média se houver possibilidade clara de agravamento, como: desmaio, dor intensa que não melhora, sangramento persistente, queimadura com bolhas, suspeita de fratura, princípio de incêndio ou ambiente com risco.
    Dificuldade para andar ou dor localizada leve sem perda de consciência não caracteriza Média, e sim Baixa.
    Regras obrigatórias:

    Nunca deixe a lista vazia — SEMPRE retorne pelo menos um serviço.  
    Os serviços devem condizer com o tipo da ocorrência (ex.: SAMU para feridos, Polícia para conflitos, Bombeiro para fogo/fumaça).  

    **Regra especial para Gravidade Baixa:**  
    - Retorne o(s) serviço(s) corretos para orientação.  
    - A descrição consolidada deve incluir claramente:  
    → “Serviço indicado apenas para ORIENTAÇÃO, sem necessidade de envio imediato de equipes.”

    3. Aqui estão alguns exemplos para detalhar como melhor avaliar as gravidades das ocorrências:
    - **Baixa:** 'Um grupo de adolescentes tá fazendo muito barulho na praça, gritando e jogando garrafas no chão. Não há briga, apenas incômodo aos moradores.'; 'Um senhor tropeçou e caiu na calçada, sofreu escoriações leves, mas está consciente e falando normalmente.'; 'Um gato está preso no telhado da casa da vizinha, mia há horas e ninguém consegue alcançá-lo.'
    - **Média:** 'Um carro suspeito está estacionado há muito tempo com dois homens observando as casas, deixando vizinhos assustados.'; 'Uma mulher desmaiou no mercado, recobrou a consciência mas permanece pálida e tonta.'; 'Um carro bateu em um poste e começou a soltar fumaça. O motorista saiu ileso, mas há cheiro de queimado e faíscas.'
    - **Alta:** 'Um homem caiu de uma escada de três metros e sente muita dor nas costas, com dormência nas pernas.'; 'Um homem armado assaltou uma moça no ponto de ônibus, empurrou-a no chão e fugiu. Ela apresenta ferimentos leves.'; 'Um incêndio começou na cozinha de um restaurante, com fumaça forte e fogo subindo nos armários.'
    - **Crítica:** 'Um homem armado mantém reféns dentro de uma loja, ameaçando atirar se alguém se aproximar.'; 'Um prédio está em chamas, com pessoas gritando por socorro e fumaça intensa.'; 'Um rapaz foi atropelado e está inconsciente no chão, com sangramento abundante.'

    4. Determine os serviços de emergência primários e secundários necessários. Use APENAS: 'Bombeiro', 'SAMU' ou 'Polícia'.

    5. Reescreva a descrição do usuário de forma:
    - Profissional  
    - Clara e objetiva  
    - Focada no que importa para o despacho  
    - Incluindo, quando for gravidade baixa, que o serviço é apenas orientativo

    6. Calcule a porcentagem inicial de risco de morte:
    Estime a probabilidade inicial de perda de vida (0% a 100%), considerando condições descritas, tempo de resposta provável e risco de agravamento.
    Use como referência para calibrar melhor a definição de gravidade:
    Gravidade	Intervalo de Risco (%)	Descrição
    Baixa	    0% - 10%	            Situações estáveis, ferimentos leves, sangramento superficial, dor leve, queda simples, pessoa consciente e conversando.
    Média	    10% - 40%	            Há dor forte, sangramento contínuo, princípio de incêndio ou possibilidade real de piora se o socorro demorar.
    Alta	    40% - 75%	            Risco evidente de morte em minutos, sem atendimento rápido.
    Crítica	    75% - 100%	            Risco imediato de morte ou múltiplas vítimas.

    Você DEVE retornar sua resposta EXCLUSIVAMENTE como um objeto JSON que obedeça ao seguinte schema: {json.dumps(json_esperado)}.
    """

    prompt_usuario = f"""
    ENDEREÇO COMPLETO: {endereco_completo}
    DESCRIÇÃO DO USUÁRIO: {descricao_usuario}
    """

    try:
        response = cliente.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": contexto_sistema},
                {"role": "user", "content": prompt_usuario}
            ],
            response_format={"type": "json_object"},
            temperature=0.0
        )
        
        resposta_json = response.choices[0].message.content
        resposta_final = json.loads(resposta_json)
        
        return resposta_final
        
    except (APIError, APIConnectionError) as e:
        print(f"DEBUG ERRO API: Falha na comunicação com a API da IA: {e}")
        erro_msg = str(e)
        if 'insufficient_quota' in erro_msg or '429' in erro_msg:
            feedback_erro = "CRÍTICO: A chave da API de Inteligência Artificial excedeu o limite de uso. Contate o administrador."
        else:
            feedback_erro = f"Falha na API ({e.__class__.__name__}). Tente novamente."
            
        return {
            "erro": feedback_erro,
            "endereco_consolidado": endereco_completo,
            "gravidade": "Indefinida",
            "servicos_acessados": [],
            "descricao_consolidada": descricao_usuario
        }
    except json.JSONDecodeError:
        print("DEBUG ERRO JSON: O modelo não retornou um JSON válido.")
        return {
            "erro": "Resposta da IA inválida. Tente novamente.",
            "endereco_consolidado": endereco_completo,
            "gravidade": "Indefinida",
            "servicos_acessados": [],
            "descricao_consolidada": descricao_usuario
        }
    except Exception as e:
        print(f"DEBUG ERRO INESPERADO: {e}")
        return {
            "erro": f"Erro inesperado: {e.__class__.__name__}. Tente novamente.",
            "endereco_consolidado": endereco_completo,
            "gravidade": "Indefinida",
            "servicos_acessados": [],
            "descricao_consolidada": descricao_usuario
        }