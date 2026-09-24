-- Use setupdb.py somente durante o desenvolvimento: ele recria esta tabela.
-- Remove a tabela anterior para que o banco possa ser reiniciado.
DROP TABLE IF EXISTS thing;

-- Cria a tabela que armazena cada treco cadastrado.
CREATE TABLE thing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    location TEXT,
    photo TEXT,
    status TEXT CHECK (status IN ('on', 'off', 'del')) DEFAULT 'on'
);

-- Insere alguns dados iniciais para testar a página inicial.
INSERT INTO thing (name, description, location, photo) VALUES
('Traquitana Junina', 'Uma coisa encontrada por aí no período das festas juninas.', 'Lá mesmo', 'https://picsum.photos/800/500?random=1'),
('Peremboca quebrada', 'Pedaço de alguma coisa, não se sabe de quê, mas é de origem terráquea.', 'Encaixotado', 'https://picsum.photos/800/500?random=2'),
('Lançador de sucata', 'No melhor estilo arma infernal, mas não funciona mais. Se é que já funcionou.', 'Bem perto', 'https://picsum.photos/800/500?random=3'),
('Pescador de linha', 'Usava quando era pequeno e não entendia para que servia. Ainda não entendo.', 'Por aí', 'https://picsum.photos/800/500?random=4');
