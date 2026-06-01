const steps = [
  {
    title: "Video Input",
    description: "User submits a YouTube video URL",
    icon: "🎥",
  },
  {
    title: "Whisper AI",
    description: "Speech is converted into text",
    icon: "🎙️",
  },
  {
    title: "OCR Engine",
    description: "Reads on-screen text from frames",
    icon: "👁️",
  },
  {
    title: "Qdrant RAG",
    description: "Retrieves FTC and YouTube policies",
    icon: "📚",
  },
  {
    title: "Groq LLM",
    description: "Performs compliance reasoning",
    icon: "🧠",
  },
  {
    title: "Audit Report",
    description: "Generates structured findings",
    icon: "📋",
  },
];

export default function HowItWorks() {
  return (
    <section className="py-28">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-4xl font-bold text-center mb-4">
          How Brand Guardian Works
        </h2>

        <p className="text-gray-400 text-center mb-16">
          A multimodal AI pipeline that analyzes content before publication.
        </p>

        <div className="grid md:grid-cols-3 gap-6">
          {steps.map((step) => (
            <div
              key={step.title}
              className="
                bg-gray-900/60
                border
                border-gray-800
                rounded-2xl
                p-6
                hover:border-blue-500
                transition-all
                duration-300
              "
            >
              <div className="text-4xl mb-4">
                {step.icon}
              </div>

              <h3 className="text-xl font-semibold mb-2">
                {step.title}
              </h3>

              <p className="text-gray-400">
                {step.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}