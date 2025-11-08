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
    1. Consolide o endereço em um formato mais curto e direto.
    2. Classifique a gravidade da situação. Use APENAS: 'Baixa', 'Média', 'Alta' ou 'Crítica'.
    3. Determine os serviços de emergência primários e secundários necessários. Use APENAS: 'Bombeiro', 'SAMU' ou 'Polícia'.
    4. Reescreva a descrição do usuário em um texto consolidado, objetivo e profissional para o despacho de equipes.

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