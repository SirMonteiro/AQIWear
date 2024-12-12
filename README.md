# AQIWear

# Introdução

## Contextualização e Motivação

Nos últimos anos, o planeta tem enfrentado uma crescente crise ambiental, caracterizada pelo aumento da poluição atmosférica, especialmente em grandes centros urbanos. A cidade de São Paulo exemplifica essa realidade, sendo uma das metrópoles mais populosas do mundo e enfrentando sérios desafios relacionados à qualidade do ar. O crescimento acelerado da frota de veículos, a industrialização, a densidade populacional e as condições climáticas contribuem para o acúmulo de poluentes no ambiente, como partículas finas (PM2,5 e PM1), dióxido de carbono (CO₂) e monóxido de carbono (CO). Esses fatores têm impacto direto na saúde pública, aumentando os casos de doenças respiratórias, cardiovasculares e outros problemas crônicos.

Nesse contexto, surge a necessidade de soluções inovadoras. O desenvolvimento de um dispositivo vestível que mede a qualidade do ar em tempo real se alinha a essa demanda urgente. Essa tecnologia não só permite que indivíduos tomem decisões mais informadas sobre os locais onde frequentam, mas também fornece dados valiosos para a comunidade científica e para o desenvolvimento de políticas públicas focadas na redução dos impactos da poluição. Em um cenário global em que a busca por cidades mais sustentáveis é prioritária, dispositivos como esse podem ser ferramentas essenciais para promover mudanças significativas e assegurar um futuro mais saudável.

A qualidade do ar na cidade de São Paulo tem se deteriorado de forma alarmante nos últimos anos, e considerando isso e as recentes notícias em que a cidade de São Paulo foi considerada a pior qualidade do ar do mundo por cerca de 4 dias consecutivos, nosso grupo propôs o desenvolvimento de um dispositivo vestível voltado para a medição em tempo real da qualidade do ar nas regiões onde o usuário transitar. Esse equipamento será capaz de coletar dados sobre os níveis de poluentes, como partículas suspensas, dióxido de carbono, monóxido de carbono, além de temperatura e umidade.

Essas informações poderão ser utilizadas para pesquisas acadêmicas e científicas, contribuindo para estudos mais aprofundados sobre os efeitos da poluição em áreas urbanas e possibilitando a elaboração de políticas públicas mais eficazes. Além disso, os próprios usuários terão acesso a esses dados, podendo evitar locais onde a qualidade do ar esteja comprometida, promovendo uma maior conscientização sobre a importância de ambientes saudáveis.

---

# Materiais e Métodos

## Parte de Tecido

### Descrição

A parte elétrica e computacional do projeto foi feita utilizando o microcontrolador **ESP32-C3** para controlar o circuito do projeto e para processar os dados coletados pelos sensores, e posteriormente enviá-los via Bluetooth Low Energy para a base de dados para que o programa possa utilizar esses dados e apresentá-los em um mapa na sua interface.

De forma geral, os componentes do projeto são:

- **ESP32-C3**: Microcontrolador conectado aos sensores e alimentado por um power bank.
- **Sensor GP2Y10**: Sensor óptico projetado para medir a concentração de partículas em suspensão no ar, como poeira e fumaça.
- **Sensor CJMCU 8118**: Módulo que combina dois sensores distintos para monitoramento da qualidade do ar:
  - CCS811: Sensor digital que mede compostos orgânicos voláteis totais (TVOC) e dióxido de carbono equivalente (eCO₂).
  - HDC1080: Sensor de temperatura e umidade relativa.
- **Power Bank**: Fonte de alimentação para o ESP32-C3.

### Lista de Materiais

| Material          | Quantidade |
|-------------------|------------|
| ESP32-C3          | 1          |
| GP2Y10            | 1          |
| CJMCU 8118        | 1          |
| Fios              | 9          |
| Cabo USB-A para USB-C | 1      |
| Power Bank        | 1          |

---

### Conexões

- **Sensor GP2Y10**:
  - Conectado ao ESP32-C3 via 4 fios:
    - **VCC** (Pino 3) -> **Vin**
    - **GND** (Pino 5) -> **GND**
    - **PM2.5** (pino 4) -> **GPIO**
    - **PM1** (pino 2) -> **GPIO**

- **Sensor CJMCU 8118**:
  - Conectado ao ESP32 via 5 fios:
    - **VCC** -> **3.3V**
    - **GND** -> **GND**
    - **SDA** -> **SDA**
    - **SCL** -> **SCL**
    - **WAK** -> **GND**

- **Bateria**:
  - Ligada ao ESP32 via cabo USB-A para USB-C.

---

## Montagem do Dispositivo

O dispositivo foi montado todo via conexão por fios, com os componentes dispostos da seguinte forma:

- **Sensor GP2Y10**: Posicionado em um bolso externo separado para exercer sua função corretamente.
- **ESP32-C3 e CJMCU 8118**: Localizados em um mesmo bolso interno.
- **Conexões**:
  - Os 4 fios do sensor GP2Y10 passam por uma canaleta interna do colete que conecta o bolso externo ao bolso interno.
  - Os fios do sensor CJMCU 8118 permanecem no mesmo bolso interno.
- **Bateria**: Alojada em um bolso interno separado e conectada por meio de uma canaleta.

---

# Resultados e conclusão

Como resultado deste protótipo, desenvolvemos um colete capaz de medir temperatura, CO2, partículas em suspensão (PM2,5) e partículas maiores (PM10). Os dados coletados são exibidos ao usuário por meio de um software desenvolvido especificamente para essa finalidade. De forma geral, o colete consegue realizar uma análise da qualidade do ar. No entanto, o sensor de temperatura e umidade apresentou uma falha na funcionalidade de medição de umidade, o que poderia ter contribuído ainda mais para a precisão da métrica, considerando a relevância da umidade na avaliação da qualidade do ar.

Além disso, implementamos a funcionalidade de exibir os dados em um mapa, de forma gráfica. Essa funcionalidade, caso houvesse mais usuários, permitiria visualizar a qualidade do ar nas regiões onde outros usuários estivessem. Dessa forma, os próprios usuários poderiam identificar e evitar áreas com baixa qualidade do ar.

Como conclusão, o desenvolvimento do colete para medir a qualidade do ar representa um avanço significativo tanto para os usuários quanto para a área de pesquisa. Para os usuários, o dispositivo oferece uma ferramenta prática e acessível para monitorar a qualidade do ar em tempo real, ajudando na prevenção de problemas respiratórios e na tomada de decisões mais informadas sobre os locais que frequentam. Essa funcionalidade é especialmente relevante para indivíduos com condições respiratórias sensíveis, como asma ou alergias, promovendo mais segurança e qualidade de vida. Para a área de pesquisa, o projeto contribui com uma abordagem inovadora para o monitoramento ambiental, fornecendo dados valiosos que podem ser utilizados em estudos sobre poluição, mudanças climáticas e saúde pública. Além disso, a integração de sensores com visualização gráfica em mapas abre caminhos para estudos de correlação entre qualidade do ar e padrões regionais, oferecendo uma base para o desenvolvimento de políticas públicas mais eficientes e sustentáveis. Este projeto demonstra o potencial de soluções tecnológicas acessíveis para unir ciência e bem-estar, trazendo benefícios diretos à sociedade e incentivando avanços no campo da pesquisa ambiental.

---

# Referências

1. [Dust Sensor DSM501A with Arduino - Maker Guides](https://www.makerguides.com/dust-sensor-dsm501a-with-arduino/)
2. [DSM501 Dust Sensor Datasheet - Elecrow](https://www.elecrow.com/download/DSM501.pdf)
3. [CCS811 GitHub Repository - Notthemarsian](https://github.com/Notthemarsian/CCS811)
4. [MicroPython HDC1080 GitHub Repository - jposada202020](https://github.com/jposada202020/MicroPython_HDC1080)
5. [ESP32 Web Bluetooth GitHub Repository - Wave1art](https://github.com/Wave1art/ESP32-Web-Bluetooth)
6. [Web Bluetooth API Documentation - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API)
