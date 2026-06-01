const pipelineSteps = [
  {
    icon: "🎥",
    title: "Video",
    description: "YouTube content input",
  },
  {
    icon: "🎙️",
    title: "Whisper",
    description: "Speech → Text",
  },
  {
    icon: "👁️",
    title: "OCR",
    description: "Frame Text Extraction",
  },
  {
    icon: "📚",
    title: "Qdrant",
    description: "Policy Retrieval",
  },
  {
    icon: "🧠",
    title: "Groq",
    description: "Compliance Reasoning",
  },
  {
    icon: "📋",
    title: "Report",
    description: "Structured Findings",
  },
];

export default function AIPipeline() {
  return (
    <section className="py-28">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-4xl font-bold text-center mb-4">
          AI Compliance Pipeline
        </h2>

        <p className="text-center text-gray-400 mb-16 max-w-3xl mx-auto">
          Every audit passes through a multimodal AI workflow that combines
          transcription, computer vision, retrieval and reasoning.
        </p>

        <div className="flex flex-wrap justify-center items-center gap-4">
          {pipelineSteps.map((step, index) => (
            <div
              key={step.title}
              className="flex items-center"
            >
              <div
                className="
                  w-52
                  h-40
                  rounded-2xl
                  border
                  border-gray-800
                  bg-gray-900/50
                  p-5
                  flex
                  flex-col
                  justify-center
                  hover:border-blue-500
                  hover:-translate-y-1
                  transition-all
                  duration-300
                "
              >
                <div className="text-4xl mb-3">
                  {step.icon}
                </div>

                <h3 className="text-xl font-semibold">
                  {step.title}
                </h3>

                <p className="text-gray-400 text-sm mt-2">
                  {step.description}
                </p>
              </div>

              {index < pipelineSteps.length - 1 && (
                <div
                  className="
                    hidden
                    lg:flex
                    text-blue-500
                    text-3xl
                    mx-3
                  "
                >
                  →
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}