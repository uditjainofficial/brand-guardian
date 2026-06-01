const technologies = [
  "LangGraph",
  "Groq",
  "Qdrant",
  "Whisper",
  "RapidOCR",
  "FastAPI",
  "React",
  "TailwindCSS",
  "TypeScript",
  "Python",
  "RAG",
  "Vector Search",
];

export default function TechStack() {
  return (
    <section className="py-28">
      <div className="max-w-5xl mx-auto text-center">
        <h2 className="text-4xl font-bold mb-4">
          Technology Stack
        </h2>

        <p className="text-gray-400 mb-12">
          Built with modern AI, backend and frontend technologies.
        </p>

        <div className="flex flex-wrap justify-center gap-4">
          {technologies.map((tech) => (
            <div
              key={tech}
              className="
                px-5
                py-3
                rounded-full
                border
                border-gray-800
                bg-gray-900/50
                text-gray-200
                hover:border-blue-500
                hover:text-white
                hover:shadow-[0_0_20px_rgba(59,130,246,0.25)]
                transition-all
                duration-300
              "
            >
              {tech}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}