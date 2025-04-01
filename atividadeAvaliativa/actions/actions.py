from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionFornecerSolucao(Action):
    def name(self) -> Text:
        return "action_fornecer_solucao"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Base de conhecimento com soluções
        base_conhecimento = {
            "acesso": [
                "1️ Vá para a página de login",
                "2️ Clique em 'Esqueci minha senha'",
                "3️ Siga as instruções no seu email",
                "Se ainda tiver dificuldades, posso transferir você para um atendente."
            ],
            "plano": [
                "🎵 Planos disponíveis:",
                "- Básico: R$10/mês (1 dispositivo)",
                "- Premium: R$20/mês (3 dispositivos)",
                "- Família: R$30/mês (6 dispositivos)",
                "Para alterar:",
                "1️ Acesse Configurações > 2️ Selecione 'Plano' > 3️ Escolha o novo plano",
            ],
            "tecnico": [
                "Vamos tentar resolver:",
                "1️ Reinicie o aplicativo",
                "2️ Verifique sua conexão com a internet",
                "3️ Atualize para a versão mais recente",
                "Se o problema persistir, descreva com mais detalhes ou posso transferir para um atendente."
            ]
        }

        # Determina o tipo de problema
        intent = tracker.latest_message['intent'].get('name')
        
        if intent == "problema_acesso":
            problema = "acesso"
        elif intent == "problema_plano":
            problema = "plano"
        elif intent == "problema_tecnico":
            problema = "tecnico"
        else:
            problema = None

        # Incrementa contador de tentativas
        tentativas = tracker.get_slot("tentativas_resolucao") or 0
        tentativas += 1
        
        if problema and problema in base_conhecimento:
            # Responde com as soluções
            for passo in base_conhecimento[problema]:
                dispatcher.utter_message(text=passo)
            
            return [SlotSet("tipo_problema", problema), SlotSet("tentativas_resolucao", 0)]
        else:
            if tentativas >= 2:
                dispatcher.utter_message(response="utter_ajuda_humana")
                return [SlotSet("tentativas_resolucao", 0)]
            else:
                dispatcher.utter_message(response="utter_pedir_mais_detalhes")
                return [SlotSet("tentativas_resolucao", tentativas)]

class ActionEncaminharHumano(Action):
    def name(self) -> Text:
        return "action_encaminhar_humano"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(response="utter_ajuda_humana")
        # Aqui integraria com sistema de tickets ou fila de atendimento
        return [SlotSet("tentativas_resolucao", 0)]