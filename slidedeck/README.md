# Anatomic3D Pitch Deck

Pitch deck em Slidev para a Anatomic3D, criado a partir do arquivo `Anatomic3D_Fase2_ProjetoDeFomento.docx`.

## Requisitos

- Node.js recomendado: 22 LTS ou superior.
- npm 10 ou superior.
- Chromium do Playwright, instalado via dependência `playwright-chromium`.

## Instalação

```bash
npm install
```

## Execução local

```bash
npm run dev
```

Abra o endereço mostrado no terminal. A apresentação usa navegação por teclado e modo apresentador nativo do Slidev.

## Edição dos textos

Edite o arquivo principal:

```text
slides.md
```

Os componentes reutilizáveis ficam em `components/` e os estilos globais em `styles/`.

## Substituição das fotografias

Substitua estes arquivos por imagens JPG quadradas, com enquadramento e iluminação semelhantes:

```text
public/team/coordenador.jpg
public/team/roberto.jpg
```

Depois, informe esses caminhos nos componentes `TeamMemberCard` do slide 11 usando `photo="/team/coordenador.jpg"` e `photo="/team/roberto.jpg"`.

Enquanto as fotos reais não forem fornecidas, o slide 11 usa placeholders SVG locais:

```text
public/team/coordenador-placeholder.svg
public/team/roberto-placeholder.svg
```

## Substituição do logotipo

Substitua:

```text
public/logos/anatomic3d.svg
```

Use SVG ou PNG local. Evite imagens por URL para não quebrar a exportação offline.

## Exportação

PDF:

```bash
npm run export:pdf
```

PPTX:

```bash
npm run export:pptx
```

PNG:

```bash
npm run export:png
```

Build estático:

```bash
npm run build
```

Preview do build:

```bash
npm run preview
```

## Publicação

### Netlify

O arquivo `netlify.toml` já aponta `npm run build` e publica a pasta `dist`.

### Vercel

Configure:

- Build command: `npm run build`
- Output directory: `dist`

### GitHub Pages

Gere o build com `npm run build` e publique o conteúdo de `dist`.

## Limitações do PPTX

A exportação PPTX do Slidev pode simplificar animações, sombras, fontes e alguns elementos Vue/SVG. Use a versão HTML como principal, PDF como versão de apresentação fixa e PPTX como formato secundário editável.

## Resolução de problemas de exportação

- Execute `npm install` novamente se o Chromium do Playwright não estiver disponível.
- Use `npm run check` para validar build e exportação PDF em sequência.
- Se houver texto cortado, reduza a quantidade de texto em `slides.md` ou ajuste os estilos em `styles/index.css`.
- Evite recursos externos por URL; mantenha imagens em `public/`.

## Dados e textos utilizados

- Fonte principal: `Anatomic3D_Fase2_ProjetoDeFomento.docx`.
- Resumo estruturado e cuidados de redação: `docs/content-source.md`.
- Roteiro de fala: `docs/presentation-script.md`.

O deck diferencia fatos atuais, metas, projeções e roadmap futuro. Números clínicos de redução de tempo ou complicações são apresentados como potenciais documentados na literatura citada no projeto, não como resultados clínicos próprios já obtidos pela Anatomic3D.
