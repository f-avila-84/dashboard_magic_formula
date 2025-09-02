// assets/clientside.js

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside_functions: {
        // Função para formatação dinâmica de números em dcc.Input
        // inputId: o ID do componente dcc.Input (e.g., 'min-volume-input')
        // inputValue: o valor atual da string digitada no dcc.Input
        formatInputLive: function(inputId, inputValue) {
            // Helper para converter string BR formatada para número puro
            function parseBrNumber(text) {
                if (typeof text !== 'string' || text.trim() === '') {
                    return 0; // Retorna 0 para string vazia ou inválida
                }
                const cleanedText = text.replace(/\./g, '').replace(/,/g, '.'); // Remove pontos de milhar, troca vírgula por ponto
                return parseFloat(cleanedText); // Converte para float
            }

            // Helper para formatar um número para o padrão BR
            function formatBrNumber(num, isInteger) {
                if (typeof num !== 'number' || isNaN(num)) {
                    return ''; // Retorna string vazia para números inválidos
                }
                const options = {
                    minimumFractionDigits: 0, // Mínimo de casas decimais
                    maximumFractionDigits: isInteger ? 0 : 2 // Máximo de casas decimais (0 para inteiro, 2 para float)
                };
                return new Intl.NumberFormat('pt-BR', options).format(num); // Usa o formatador internacional para pt-BR
            }

            // Encontra o elemento DOM real do input para obter a posição do cursor
            const inputElement = document.getElementById(inputId);
            if (!inputElement) {
                throw window.dash_clientside.PreventUpdate; // Previne atualização desnecessária se o elemento não existe
            }

            // Determina se o input é para inteiro ou float com base no seu ID
            const isIntegerInput = (inputId === 'min-volume-input');

            // Salva o valor original para comparação posterior
            const originalValue = inputValue;

            // Converte o valor digitado para número e depois formata de volta
            const parsedNum = parseBrNumber(originalValue);
            let newFormattedValue = formatBrNumber(parsedNum, isIntegerInput);

            // Tratamento especial para o caso do usuário digitar vírgula em um campo float
            // Ex: "1000" -> o usuário digita "," -> "1.000," (ao invés de "1.000,00" ou "1.000")
            if (!isIntegerInput && originalValue.endsWith(',') && parsedNum === Math.floor(parsedNum)) {
                newFormattedValue += ',';
            }
            
            // Previne um loop infinito de callback e o piscar do cursor se o valor formatado
            // for o mesmo que o valor original (sem alteração de formatação)
            if (newFormattedValue === originalValue) {
                throw window.dash_clientside.PreventUpdate;
            }

            // Retorna apenas a string
            return newFormattedValue; 
        }
    }
});