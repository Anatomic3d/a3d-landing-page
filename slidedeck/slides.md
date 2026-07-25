---
theme: default
title: Anatomic3D Pitch Deck
info: Modelagem anatomica personalizada para planejamento cirurgico e reducao de risco hemorragico
aspectRatio: 16/9
canvasWidth: 1920
transition: fade
download: true
fonts:
  sans: Inter
---

<section class="hero-grid">
  <div>
    <div class="logo-space">
      <img src="/logos/anatomic3d.svg" alt="Logotipo Anatomic3D" />
      <span>Anatomic3D</span>
    </div>
    <h1 class="title" style="margin-top: 78px;">Modelagem anatômica personalizada para planejamento cirúrgico e redução de risco hemorrágico</h1>
    <p class="subtitle">IA, processamento de imagens médicas e impressão 3D aplicados à segurança cirúrgica.</p>
    <div class="chips" style="margin-top: 46px;">
      <span class="chip">Projeto de Fomento - Fase 2</span>
      <span class="chip">Centelha 3 Rondônia</span>
      <span class="chip">Vilhena - Rondônia</span>
    </div>
  </div>
  <div class="visual-panel surface" aria-label="Ilustração anatômica tridimensional abstrata">
    <img class="mesh-bg" src="/images/dicom-to-3d.svg" alt="" />
    <img src="/images/anatomy-mesh.svg" alt="Modelo anatômico tridimensional abstrato" />
  </div>
</section>

<!--
Mensagem central: apresentar a Anatomic3D como tecnologia médica que transforma exames de imagem em modelos anatômicos personalizados para apoiar planejamento cirúrgico. A fala deve situar o projeto no Centelha 3 Rondônia, reforçar a origem em Vilhena e deixar claro que a solução apoia a decisão clínica, sem substituir o cirurgião.
-->

---

<section class="slide-shell">
  <SectionLabel text="Problema clínico" />
  <h2 class="slide-title">Cirurgias complexas ainda são planejadas a partir de imagens bidimensionais</h2>
  <div class="two-col" style="grid-template-columns: 1.08fr .92fr; gap: 42px;">
    <div>
      <p class="lead">Tomografia e ressonância contêm informação tridimensional, mas grande parte do planejamento pré-operatório ainda acontece em cortes 2D.</p>
      <div class="cards-4" style="margin-top: 40px;">
        <FeatureCard v-click title="Incerteza anatômica" icon="scan" text="Relações espaciais entre estruturas críticas ficam mais difíceis de compreender." compact />
        <FeatureCard v-click title="Maior tempo de sala" icon="hospital" text="Decisões relevantes podem migrar para dentro do procedimento." compact />
        <FeatureCard v-click title="Risco hemorrágico" icon="blood" text="Menor previsibilidade sobre vasos, estruturas e trajetórias cirúrgicas." compact />
        <FeatureCard v-click title="Custos assistenciais" icon="revenue" text="Tempo cirúrgico, hemocomponentes e complicações impactam o custo." compact />
      </div>
    </div>
    <div class="surface" style="padding: 34px; min-height: 565px; display: grid; place-items: center;">
      <img src="/images/dicom-to-3d.svg" alt="Comparação entre cortes DICOM e modelo 3D personalizado" style="width: 100%;" />
    </div>
  </div>
</section>

<!--
Mensagem central: o problema é espacial, não apenas tecnológico. Explique que a solução não substitui diagnóstico, julgamento médico ou decisão cirúrgica; ela adiciona uma representação física e tridimensional da anatomia individual para reduzir incerteza antes da cirurgia.
-->

---

<section class="slide-shell">
  <SectionLabel text="Solução" />
  <h2 class="slide-title">Do exame médico ao modelo anatômico personalizado</h2>
  <p class="lead" style="max-width: 1260px;">A Anatomic3D transforma dados de tomografia e ressonância em modelos físicos ou digitais de alta fidelidade para planejamento pré-operatório.</p>
  <div class="pipeline" style="margin-top: 20px;">
    <ProcessStep v-click index="1" title="DICOM" icon="scan" text="Recebimento dos exames de CT ou MRI." />
    <ProcessStep v-click index="2" title="Segmentação por IA" icon="ai" text="Identificação das estruturas anatômicas de interesse." />
    <ProcessStep v-click index="3" title="Malha tridimensional" icon="cube" text="Conversão dos volumes segmentados em STL ou OBJ." />
    <ProcessStep v-click index="4" title="Validação técnica" icon="check" text="Refinamento, controle de qualidade e preparação do modelo." />
    <ProcessStep v-click index="5" title="Entrega clínica" icon="print" text="Modelo físico, arquivo digital ou aplicação de planejamento." />
  </div>
  <div class="chain" style="margin-top: 18px;">
    <span>Anatomia individual</span><b class="arrow">→</b>
    <span>melhor compreensão espacial</span><b class="arrow">→</b>
    <span>planejamento mais previsível</span>
  </div>
</section>

<!--
Mensagem central: o pipeline combina automação e revisão. Destaque que a segmentação por IA acelera o processo, mas a qualidade clínica depende de revisão humana, controle técnico e preparação adequada para cada necessidade cirúrgica.
-->

---

<section class="slide-shell">
  <SectionLabel text="Timing" />
  <h2 class="slide-title">A convergência tecnológica tornou a solução viável</h2>
  <div class="quadrants" style="height: 640px; margin-top: 16px;">
    <FeatureCard v-click title="IA para segmentação" icon="ai" text="Modelos pré-treinados reduzem significativamente o trabalho manual de segmentação." />
    <FeatureCard v-click title="Ferramentas open source" icon="cube" text="Ecossistema científico maduro para processamento e reconstrução de imagens médicas." />
    <FeatureCard v-click title="Impressão 3D acessível" icon="print" text="Equipamentos de maior precisão estão mais disponíveis para operação regional." />
    <FeatureCard v-click title="Pressão por eficiência" icon="hospital" text="Hospitais buscam reduzir tempo, complicações e custos assistenciais." />
    <div class="center-chip">Momento de oportunidade</div>
  </div>
  <QuoteHighlight text="Tecnologias antes restritas a grandes centros podem ser estruturadas regionalmente e escaladas digitalmente." />
</section>

<!--
Mensagem central: o momento é favorável porque várias tecnologias amadureceram ao mesmo tempo. Conecte IA, software científico aberto, impressão 3D e necessidade de eficiência hospitalar, explicando por que Vilhena pode iniciar a validação regional com potencial de escala posterior.
-->

---

<section class="slide-shell">
  <SectionLabel text="Valor clínico" />
  <h2 class="slide-title">Mais informação antes da cirurgia</h2>
  <div class="two-col" style="grid-template-columns: .86fr 1.14fr; gap: 42px;">
    <MetricCard label="Potencial de redução no tempo de sala" value="15% a 35%" icon="hospital" detail="Estimativa documentada na literatura mencionada no projeto; resultado regional ainda será avaliado nos casos piloto." />
    <div>
      <div class="chain" style="flex-wrap: wrap;">
        <span>Modelo personalizado</span><b class="arrow">→</b>
        <span>melhor visualização</span><b class="arrow">→</b>
        <span>planejamento mais preciso</span><b class="arrow">→</b>
        <span>menor incerteza intraoperatória</span>
      </div>
      <div class="cards-4" style="margin-top: 34px;">
        <FeatureCard title="Hemocomponentes" icon="blood" text="Potencial redução do uso intraoperatório." compact />
        <FeatureCard title="Transfusões" icon="check" text="Menor exposição do paciente a transfusões desnecessárias." compact />
        <FeatureCard title="Complicações" icon="hospital" text="Potencial redução de complicações e reinternações." compact />
        <FeatureCard title="PBM" icon="scan" text="Apoio às estratégias de Patient Blood Management." compact />
      </div>
      <p class="micro" style="margin-top: 18px;">Nota: benefícios apresentados como potencial documentado na literatura citada no projeto, não como resultado clínico já obtido pela Anatomic3D.</p>
    </div>
  </div>
</section>

<!--
Mensagem central: separar evidência geral de validação local. Apresente os números como potencial indicado pela literatura e explique que os resultados próprios da Anatomic3D serão avaliados nos casos piloto previstos no projeto, com foco em segurança, previsibilidade e PBM.
-->

---

<section class="slide-shell">
  <SectionLabel text="Produto" />
  <h2 class="slide-title">Uma solução, diferentes formas de entrega</h2>
  <div class="cards-3" style="margin-top: 28px;">
    <FeatureCard title="Modelo físico" icon="print" text="Anatomia personalizada impressa em PLA ou resina para planejamento, treinamento e comunicação multidisciplinar." />
    <FeatureCard title="Modelo digital" icon="cube" text="Arquivo STL ou OBJ com visualização tridimensional, entrega remota e base para escala nacional." />
    <FeatureCard title="Aplicações especializadas" icon="scan" text="Guias de corte personalizados, cortes virtuais, planejamento de trajetórias e materiais para treinamento." />
  </div>
  <div class="surface" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; padding: 24px; margin-top: 28px;">
    <img src="/images/anatomy-mesh.svg" alt="Render abstrato de modelo físico" style="height: 260px; margin: auto;" />
    <img src="/images/dicom-to-3d.svg" alt="Representação de entrega digital" style="height: 260px; margin: auto;" />
    <img src="/images/anatomy-mesh.svg" alt="Representação de aplicação especializada" style="height: 260px; margin: auto; transform: scaleX(-1);" />
  </div>
  <p class="micro">Os entregáveis dependem da necessidade clínica, da estrutura anatômica e do estágio de desenvolvimento do serviço.</p>
</section>

<!--
Mensagem central: a mesma base técnica pode gerar diferentes entregáveis. Explique que o modelo físico atende planejamento e comunicação, o digital viabiliza entrega remota e o roadmap inclui aplicações especializadas conforme necessidade clínica e maturidade do serviço.
-->

---

<section class="slide-shell">
  <SectionLabel text="Tecnologia" />
  <h2 class="slide-title">Pipeline baseado em IA, computação científica e impressão 3D</h2>
  <div class="layers" style="margin-top: 14px;">
    <div class="tech-layer"><strong>Aquisição</strong><div class="chips"><span class="chip">3D Slicer</span><span class="chip">DICOM</span><span class="chip">CT e MRI</span></div></div>
    <div class="tech-layer"><strong>Segmentação</strong><div class="chips"><span class="chip">3D Slicer Segment Editor</span><span class="chip">ITK-SNAP</span><span class="chip">MONAI</span><span class="chip">MONAI Label</span><span class="chip">TotalSegmentator</span></div></div>
    <div class="tech-layer"><strong>Malha e refinamento</strong><div class="chips"><span class="chip">Marching Cubes</span><span class="chip">MeshLab</span><span class="chip">Blender</span></div></div>
    <div class="tech-layer"><strong>Planejamento</strong><div class="chips"><span class="chip">SlicerIGT</span><span class="chip">BoneReconstructionPlanner</span><span class="chip">OpenIGTLink</span></div></div>
    <div class="tech-layer"><strong>Saída clínica</strong><div class="chips"><span class="chip">STL/OBJ</span><span class="chip">PLA</span><span class="chip">Resina</span><span class="chip">Guias personalizados</span><span class="chip">Entrega digital</span></div></div>
  </div>
  <QuoteHighlight text="Uma stack open source reduz custos de licenciamento e permite evolução tecnológica contínua." />
</section>

<!--
Mensagem central: a base tecnológica é concreta e alinhada ao documento. Destaque a segmentação como etapa crítica, explique o papel da IA e reforce que automação deve permanecer associada a revisão técnica e controle de qualidade.
-->

---

<section class="slide-shell">
  <SectionLabel text="Diferenciais" />
  <h2 class="slide-title">Por que a Anatomic3D é diferente</h2>
  <div class="cards-6" style="margin-top: 28px;">
    <FeatureCard title="Personalização total" icon="brain" text="Cada modelo representa a anatomia individual do paciente." compact />
    <FeatureCard title="Aplicação clínica" icon="hospital" text="Solução orientada ao planejamento pré-operatório." compact />
    <FeatureCard title="Integração com PBM" icon="blood" text="Contribui para redução de risco hemorrágico e uso racional de hemocomponentes." compact />
    <FeatureCard title="Stack open source" icon="cube" text="Menor dependência de licenças proprietárias." compact />
    <FeatureCard title="Ineditismo regional" icon="map" text="Proposta de estruturar oferta especializada no Cone Sul de Rondônia." compact />
    <FeatureCard title="Roadmap SaaS" icon="cloud" text="Evolução planejada para plataforma digital escalável." compact />
  </div>
</section>

<!--
Mensagem central: os diferenciais combinam foco clínico, personalização e caminho de escala. Use ineditismo regional com cuidado, como proposta de estruturação no Cone Sul de Rondônia, sem afirmar exclusividade nacional ou parcerias já consolidadas.
-->

---

<section class="slide-shell">
  <SectionLabel text="Mercado inicial" />
  <h2 class="slide-title">Validação regional, potencial de expansão nacional</h2>
  <div class="market-grid" style="margin-top: 22px;">
    <div class="surface" style="padding: 30px;">
      <h3 style="font-size: 30px; margin: 0 0 18px; color: var(--color-primary-dark);">Vilhena e Cone Sul de Rondônia</h3>
      <div class="chips" style="margin-bottom: 18px;"><span class="chip">hospitais</span><span class="chip">imagem diagnóstica</span><span class="chip">clínicas cirúrgicas</span><span class="chip">operadoras</span><span class="chip">ensino</span></div>
      <p class="body">Instituições de interesse ou potenciais parceiras: Hospital Regional Adamastor Teixeira de Oliveira, Hospital Cooperar/Unimed Vilhena e clínicas de diagnóstico por imagem da região.</p>
      <p class="micro" style="margin-top: 16px;">Não apresentadas como clientes formalizados neste deck.</p>
    </div>
    <div class="surface" style="padding: 30px; display: grid; grid-template-columns: .9fr 1.1fr; gap: 24px; align-items: center;">
      <div style="min-height: 360px; display: grid; place-items: center;">
        <svg width="340" height="380" viewBox="0 0 340 380" fill="none" role="img" aria-label="Mapa estilizado de Rondônia com destaque para Vilhena">
          <path d="M70 44 264 82 300 206 202 330 72 280 36 152Z" fill="#E8F3F5" stroke="#0E5A68" stroke-width="6"/>
          <circle cx="142" cy="272" r="18" fill="#45B7A8" stroke="#0E5A68" stroke-width="5"/>
          <text x="168" y="280" font-size="24" fill="#083F49" font-weight="700">Vilhena</text>
          <path d="M205 78C250 35 286 27 316 20" stroke="#1E88A8" stroke-width="7" stroke-linecap="round"/>
          <path d="M296 12 320 19 305 39" stroke="#1E88A8" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <div>
        <h3 style="font-size: 30px; margin: 0 0 18px; color: var(--color-primary-dark);">Expansão</h3>
        <p class="body">Região Norte, hospitais fora dos grandes centros, entrega digital de modelos, futura plataforma SaaS e alcance nacional.</p>
        <QuoteHighlight text="Começar perto para validar. Escalar digitalmente para ampliar o alcance." />
      </div>
    </div>
  </div>
</section>

<!--
Mensagem central: a estratégia começa regional e escala digitalmente. Explique que hospitais e clínicas citados são mercado inicial ou potenciais parceiros, conforme o documento, e que a expansão nacional depende da plataforma SaaS pós-projeto.
-->

---

<section class="slide-shell">
  <SectionLabel text="Modelo de negócio" />
  <h2 class="slide-title">Receita recorrente com evolução para SaaS</h2>
  <div class="cards-4" style="margin-top: 10px;">
    <RevenueCard title="Cobrança por projeto" icon="cube" text="Modelo personalizado por caso clínico." />
    <RevenueCard title="Pacotes institucionais" icon="hospital" text="Contratos mensais com volume definido." />
    <RevenueCard title="Plataforma SaaS" icon="cloud" text="Assinatura mensal ou pagamento por uso." />
    <RevenueCard title="Complementares" icon="print" text="Guias, treinamento e materiais didáticos." />
  </div>
  <div class="scenario-grid" style="margin-top: 24px;">
    <div class="scenario surface">
      <h3>Conservador</h3>
      <p class="micro">Projeção: 4 casos/mês x R$ 1.500</p>
      <div class="amount">R$ 6 mil/mês</div>
      <p class="micro">Custo fixo estimado: ~R$ 4 mil</p>
    </div>
    <div class="scenario surface">
      <h3>Moderado</h3>
      <p class="micro">Projeção: 10 casos/mês x R$ 1.500</p>
      <div class="amount">R$ 15 mil/mês</div>
      <p class="micro">Custo fixo estimado: ~R$ 6 mil</p>
    </div>
    <div class="scenario surface">
      <h3>SaaS pós-projeto</h3>
      <p class="micro">Projeção: 50+ casos/mês x R$ 600</p>
      <div class="amount">R$ 30 mil+/mês</div>
      <p class="micro">Custo fixo estimado: ~R$ 8 mil</p>
    </div>
  </div>
  <p class="micro" style="margin-top: 12px;">Todos os valores deste slide são projeções financeiras do projeto.</p>
</section>

<!--
Mensagem central: o negócio começa como serviço especializado e ganha recorrência e escala com automação. Deixe explícito que os cenários financeiros são projeções, não faturamento realizado, e que o SaaS é etapa pós-projeto.
-->

---

<section class="slide-shell">
  <SectionLabel text="Equipe executora" />
  <h2 class="slide-title">Competências complementares para executar a visão</h2>
  <div class="team-grid" style="margin-top: 8px;">
    <TeamMemberCard
      photo="/team/coordenador-placeholder.svg"
      photoLabel="Adicionar foto do coordenador"
      name="[INSERIR NOME DO COORDENADOR]"
      formation="Doutor em Ciência da Computação"
      role="Coordenador, responsável técnico, estratégico, comercial e administrativo."
      :skills="['inteligência artificial','redes neurais convolucionais','segmentação médica','processamento de imagens','malhas 3D','computação científica','engenharia de software','arquitetura SaaS']"
      responsibility="Liderança tecnológica, integração do pipeline e desenvolvimento do produto."
    />
    <TeamMemberCard
      photo="/team/roberto-placeholder.svg"
      photoLabel="Adicionar foto de Roberto"
      name="Roberto Simplício Guimarães"
      formation="Analista de Sistemas e Mestre em Engenharia Nuclear pelo IPEN/USP"
      role="Bolsista CNPq e responsável pelo apoio técnico-operacional."
      :skills="['computação científica','física da tomografia','processamento de imagens médicas','segmentação anatômica','modelagem tridimensional','pós-processamento','controle de qualidade','pipeline SaaS']"
      responsibility="Operação técnica, validação do pipeline e controle de qualidade dos modelos."
    />
  </div>
  <div class="complement">
    <span>IA + Engenharia de Software</span><span>×</span><span>Imagem Médica + Computação Científica</span><span>=</span><span>Tecnologia aplicada ao planejamento cirúrgico</span>
  </div>
</section>

<!--
Mensagem central: a equipe tem complementaridade técnica direta para executar o pipeline. Explique que o coordenador lidera IA, software e produto, enquanto Roberto apoia operação técnica, imagem médica, computação científica e controle de qualidade. Não use percentuais subjetivos.
-->

---

<section class="slide-shell">
  <SectionLabel text="Roadmap" />
  <h2 class="slide-title">Da validação regional à plataforma SaaS</h2>
  <div class="roadmap-grid" style="margin-top: 22px;">
    <RoadmapPhase
      v-click
      phase="Fase 1"
      period="Meses 1 a 6"
      title="Serviço assistido"
      :goals="['implantação da infraestrutura','segmentação semiautomática','revisão humana','impressão e entrega','processos internos','meta de pelo menos cinco casos piloto','busca de parcerias regionais']"
      milestone="Pipeline clínico-operacional validado."
    />
    <RoadmapPhase
      v-click
      phase="Fase 2"
      period="Meses 7 a 12"
      title="Serviço escalado"
      :goals="['adoção mais ampla dos modelos de IA','início da operação comercial','primeiros pedidos ou contratos pagos','contrato institucional recorrente','protótipo funcional do pipeline SaaS']"
      milestone="Operação comercial regional e MVP digital."
    />
    <RoadmapPhase
      v-click
      phase="Fase 3"
      period="Pós-projeto"
      title="Plataforma SaaS"
      :goals="['upload de DICOM','segmentação automática','geração sob demanda','entrega digital','assinatura ou pay-per-use','alcance nacional']"
      milestone="Escala sem crescimento proporcional da operação física."
      future
    />
  </div>
</section>

<!--
Mensagem central: o roadmap tem duas fases dentro dos 12 meses e uma terceira pós-projeto. Reforce que casos piloto, contratos e SaaS são metas, não resultados já conquistados, e que a validação regional antecede a escala nacional.
-->

---

<section class="slide-shell">
  <SectionLabel text="Investimento" />
  <h2 class="slide-title">R$ 80 mil para transformar validação técnica em operação</h2>
  <div class="budget-layout" style="margin-top: 18px;">
    <div class="surface" style="padding: 30px;">
      <BudgetBar label="Equipamentos e material permanente" value="R$ 52.400" :percent="65.50" color="#0E5A68" />
      <BudgetBar label="Material de consumo" value="R$ 17.000" :percent="21.25" color="#1E88A8" />
      <BudgetBar label="Serviços de terceiros" value="R$ 4.000" :percent="5.00" color="#45B7A8" />
      <BudgetBar label="Contabilidade" value="R$ 3.600" :percent="4.50" color="#7BAEB8" />
      <BudgetBar label="Diárias e locomoção" value="R$ 3.000" :percent="3.75" color="#A7C8CE" />
      <div class="cards-3" style="margin-top: 24px;">
        <MetricCard label="Subvenção" value="R$ 80 mil" detail="Total da subvenção econômica." icon="revenue" />
        <MetricCard label="Contrapartida" value="R$ 4 mil" detail="Recursos próprios, 5% da subvenção." icon="check" />
        <MetricCard label="Bolsa CNPq" value="R$ 50 mil" detail="Fonte separada; não compõe a subvenção." icon="team" />
      </div>
    </div>
    <div>
      <p class="closing">Transformar exames médicos em modelos anatômicos personalizados para cirurgias mais seguras, previsíveis e acessíveis.</p>
      <div class="chips" style="margin: 32px 0;">
        <span class="chip">Validar regionalmente</span>
        <span class="chip">Estruturar a operação</span>
        <span class="chip">Preparar a escala nacional</span>
      </div>
      <QuoteHighlight text="Anatomic3D" note="Tecnologia médica desenvolvida em Rondônia para ampliar a segurança cirúrgica." />
      <div class="contact-row">
        <div class="contact-slot">Coordenador</div>
        <div class="contact-slot">E-mail</div>
        <div class="contact-slot">Telefone</div>
        <div class="contact-slot">Site</div>
        <div class="contact-slot">QR Code</div>
      </div>
    </div>
  </div>
</section>

<!--
Mensagem central: o fomento compra capacidade operacional e reduz risco de execução. Explique a subvenção de R$ 80 mil separadamente da contrapartida de R$ 4 mil e da bolsa CNPq de R$ 50 mil, que vem de fonte distinta. Feche com validação regional, operação e escala nacional.
-->
