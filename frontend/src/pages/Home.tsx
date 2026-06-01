import Hero from "../components/Hero";
import AuditForm from "../components/AuditForm";
import HowItWorks from "../components/HowItWorks";
import AIPipeline from "../components/AIPipeline";
import TechStack from "../components/TechStack";
import Footer from "../components/Footer";

export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white">
      <div className="container mx-auto px-6">
        <Hero />

        <AuditForm />

        <AIPipeline />

        <HowItWorks />

        <TechStack />
      </div>

      <Footer />
    </main>
  );
}