import { useState } from "react";
import { Button, Rows, Text, MultilineInput, CharacterCountDecorator } from "@canva/app-ui-kit";
import styles from "styles/components.css";

// Definição de tipo para o item da análise
interface AnalysisItem {
  item: string;
}

export const App = () => {
  const [prompt, setPrompt] = useState("teste");
  const [videoType, setVideoType] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [videoGenerated, setVideoGenerated] = useState(false);
  const [videoUrl, setVideoUrl] = useState("");
  const [showAnalysis, setShowAnalysis] = useState(false);
  const [analysisData, setAnalysisData] = useState<AnalysisItem[]>([]);

  const handleGenerateVideo = async () => {
    setIsLoading(true);
    // Lógica para geração de vídeo

    try {
      const response = await fetch("http://localhost:8000/generate-video/", { // Atualize o URL para o backend
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt,
          videoType
        }),
      });

      if (!response.ok) {
        throw new Error("Erro ao gerar vídeo");
      }

      const data = await response.json();
      setVideoUrl(data.videoUrl); // Certifique-se de que o backend retorna a URL do vídeo
      setVideoGenerated(true);
    } catch (error) {
      console.error("Erro ao gerar vídeo:", error);
    } finally {
      setIsLoading(false);
    }

    setTimeout(() => {
      setIsLoading(false);
      setVideoGenerated(true);
      setVideoUrl("url_do_video_gerado.mp4");
    }, 2000);
  };

  const handleAnalyzeVideo = () => {
    // Implementar lógica de análise do vídeo aqui    
    setAnalysisData([{ item: "Exemplo 1" }, { item: "Exemplo 2" }]);
    setShowAnalysis(true);
  };

  return (
    <div className={styles.scrollContainer}>
      <Rows spacing="2u">
        <Text>
          Insira o prompt para o gerador de vídeo.
        </Text>
        <label>
          Tipo de Vídeo:
          <select value={videoType} onChange={(e) => setVideoType(e.target.value)}>
            <option value="">Selecione um tipo</option>
            <option value="tipo1">Tipo 1</option>
            <option value="tipo2">Tipo 2</option>
            <option value="tipo3">Tipo 3</option>
          </select>
        </label>
        <MultilineInput
          footer={<CharacterCountDecorator max={500} />}
          onChange={(value) => setPrompt(value)}
          placeholder="Seu Prompt"
          value={prompt}
        />
        <Button variant="primary" onClick={handleGenerateVideo} stretch>
          Gerar Vídeo
        </Button>

        {isLoading && <Text>Generate the Video...</Text>}

        {!isLoading && videoGenerated && (
          <>
            <video src={videoUrl} controls />
            <MultilineInput
              footer={<CharacterCountDecorator max={500} />}
              onChange={(value) => setPrompt(value)}
              placeholder="Seu Prompt"
              value={prompt}
            />
            <Button variant="primary" onClick={handleGenerateVideo} stretch>
              Regenerate Vídeo
            </Button>
            <Button variant="primary" onClick={handleAnalyzeVideo} stretch>
              Analisar Vídeo
            </Button>
          </>
        )}

        {showAnalysis && (
          <>
            <table>
              <thead>
                <tr>
                  <th>Itens Gerados</th>
                </tr>
              </thead>
              <tbody>
                {analysisData.map((data, index) => (
                  <tr key={index}>
                    <td>{data.item}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <Button variant="secondary" onClick={() => setShowAnalysis(false)} stretch>
              Voltar
            </Button>
            <Button variant="primary" onClick={() => { /* Lógica para upload de updates */ }} stretch>
              Upload Updates
            </Button>
          </>
        )}
      </Rows>
    </div>
  );
};
