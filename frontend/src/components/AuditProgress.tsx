interface AuditProgressProps {
  step: string;
}

export default function AuditProgress({
  step,
}: AuditProgressProps) {
  return (
    <div
      className="
        fixed
        inset-0
        bg-black/80
        backdrop-blur-sm
        flex
        items-center
        justify-center
        z-50
      "
    >
      <div
        className="
          w-full
          max-w-lg
          rounded-2xl
          border
          border-zinc-800
          bg-zinc-950
          p-8
          text-center
        "
      >
        <div
          className="
            mx-auto
            mb-6
            h-12
            w-12
            animate-spin
            rounded-full
            border-4
            border-blue-500
            border-t-transparent
          "
        />

        <h2 className="text-2xl font-bold text-white mb-4">
          Running Compliance Audit
        </h2>

        <p className="text-blue-400 text-lg">
          {step}
        </p>

        <p className="text-gray-500 mt-4 text-sm">
          This may take a few moments depending on
          video length.
        </p>
      </div>
    </div>
  );
}