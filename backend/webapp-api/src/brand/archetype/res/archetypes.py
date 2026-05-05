from typing import Final

from src.brand.archetype.model import (
    BrandArchetype,
    BrandArchetypeData,
    BrandArchetypeName,
)


ARCHETYPE_DATA: Final[dict[BrandArchetypeName, BrandArchetype]] = {
    BrandArchetypeName.INNOCENT: BrandArchetype(
        name=BrandArchetypeName.INNOCENT,
        data=BrandArchetypeData(
            base_human_need=(
                "Safety, simplicity, goodness; desire for a worry-free life "
                "and predictable happiness."
            ),
            archetype_description=(
                "Promises peace of mind and a return to what feels pure and "
                "uncomplicated. Removes friction, reduces risk, and creates a sense "
                "of childlike optimism—'the world can be good, and we can trust it.' "
                "Often positioned as the ethical or 'clean' choice."
            ),
            identification_clues=(
                "Look for 'simple, pure, gentle, natural, clean,' trust "
                "marks/certifications. Minimalist layouts with whitespace and soft "
                "imagery; effortless onboarding. Safety cues prominent; tone avoids "
                "conflict or drama."
            ),
            core_shared_values=(
                "Simplicity, transparency, honesty, kindness, optimism, "
                "trustworthiness, responsibility to people and planet."
            ),
            typical_target_audience=(
                "Families; wellness/natural-living consumers; mainstream, risk-averse "
                "buyers; broad appeal."
            ),
            colors_graphics_description=(
                "Whites/pastels; airy spacing; rounded shapes; soft gradients; natural "
                "textures (cotton/clouds/water). Friendly sans-serif type; "
                "approachable line icons."
            ),
            writing_style_description=(
                "Plain-spoken, reassuring, gentle; short sentences and everyday words. "
                "'We make good choices so you don't have to.' Avoids hype or "
                "confrontation."
            ),
            examples="Innocent Drinks, The Honest Company, Ivory",
        ),
    ),
    BrandArchetypeName.EVERYMAN: BrandArchetype(
        name=BrandArchetypeName.EVERYMAN,
        data=BrandArchetypeData(
            base_human_need=(
                "Belonging, acceptance, fairness; comfort of fitting in without pretense."
            ),
            archetype_description=(
                "Down-to-earth practicality and inclusivity. Rejects elitism and "
                "promises reliable value that works in real life; like a friendly "
                "neighbor."
            ),
            identification_clues=(
                "Relatable imagery, no-nonsense design, straightforward pricing. Avoids "
                "jargon and luxury cues; covers common needs."
            ),
            core_shared_values=(
                "Authenticity, humility, equality, practicality, reliability, value "
                "for money."
            ),
            typical_target_audience=(
                "Mass-market, value-conscious shoppers across ages; "
                "family/community-oriented."
            ),
            colors_graphics_description=(
                "Comfortable blues/grays; simple grids; approachable photography. "
                "Sturdy sans-serif; clear universal icons."
            ),
            writing_style_description=(
                "Conversational, friendly, unpretentious—'we've got your back.' Focus "
                "on usefulness, durability, fairness; no buzzwords."
            ),
            examples="IKEA, Walmart, Levi's",
        ),
    ),
    BrandArchetypeName.HERO: BrandArchetype(
        name=BrandArchetypeName.HERO,
        data=BrandArchetypeData(
            base_human_need=(
                "Mastery, courage, achievement; desire to prove worth through brave action."
            ),
            archetype_description=(
                "Inspires people to push limits and overcome obstacles. Customer is "
                "the protagonist; performance, endurance, excellence are central."
            ),
            identification_clues=(
                "Bold CTAs, power verbs, performance stats, athlete/challenger "
                "narratives. High contrast visuals, dynamic angles, triumphant "
                "before/after metrics."
            ),
            core_shared_values=(
                "Courage, discipline, perseverance, achievement, impact, meritocracy."
            ),
            typical_target_audience=(
                "Athletes, high-performing professionals, ambitious students; "
                "competitive, goal-oriented."
            ),
            colors_graphics_description=(
                "Reds/blacks/deep blues; strong contrast; angular shapes; motion blur "
                "and directional lines. Condensed bold type."
            ),
            writing_style_description=(
                "Motivational and challenging—'prove it,' 'rise to the occasion.' "
                "Clear outcomes, training frameworks, performance claims."
            ),
            examples="Nike, Under Armour, U.S. Army",
        ),
    ),
    BrandArchetypeName.OUTLAW: BrandArchetype(
        name=BrandArchetypeName.OUTLAW,
        data=BrandArchetypeData(
            base_human_need=(
                "Liberation, independence; rebellion against constraints and conformity."
            ),
            archetype_description=(
                "Challenges the status quo, provokes, and attracts non-conformists. "
                "Taps into subcultures and turns tension with the mainstream into a "
                "badge of honor."
            ),
            identification_clues=(
                "Defiant headlines, taboo-testing visuals, anti-establishment messages. "
                "Raw textures, DIY aesthetics, disruptive drops/collabs."
            ),
            core_shared_values=(
                "Freedom, authenticity, self-expression, disruption, loyalty to the tribe."
            ),
            typical_target_audience=(
                "Youthful/countercultural segments; early adopters; collectors; "
                "identity-driven subcultures."
            ),
            colors_graphics_description=(
                "Black/red/stark white; distressed textures, graffiti/sticker layers, "
                "photocopy effects. Bold/condensed, sometimes 'imperfect' type."
            ),
            writing_style_description=(
                "Provocative, witty, punchy; 'them vs. us.' Encourages rule-breaking; "
                "avoids corporate speak/long explanations."
            ),
            examples="Harley-Davidson, Diesel, Supreme",
        ),
    ),
    BrandArchetypeName.EXPLORER: BrandArchetype(
        name=BrandArchetypeName.EXPLORER,
        data=BrandArchetypeData(
            base_human_need=(
                "Freedom, discovery, self-direction; seeking meaning via new experiences."
            ),
            archetype_description=(
                "Invites people to step beyond the familiar and find themselves. "
                "Celebrates autonomy, curiosity, and resilience in nature or life's "
                "open spaces."
            ),
            identification_clues=(
                "Wide-angle vistas, maps/topographic lines, gear details. Copy: 'find "
                "your path,' 'go further'; emphasizes personal choice."
            ),
            core_shared_values=(
                "Autonomy, authenticity, curiosity, respect for nature, resilience, "
                "self-reliance."
            ),
            typical_target_audience=(
                "Outdoor enthusiasts, travelers, digital nomads, self-directed "
                "professionals; higher spend on gear/experiences."
            ),
            colors_graphics_description=(
                "Earth tones, forest greens, sky blues; natural textures "
                "(leather/canvas/wood). Practical, rugged typography; horizon/journey "
                "photography."
            ),
            writing_style_description=(
                "Aspirational but grounded; sensory detail and concrete tips. Avoids "
                "prescriptive 'one right way.'"
            ),
            examples="The North Face, Patagonia, Land Rover",
        ),
    ),
    BrandArchetypeName.CREATOR: BrandArchetype(
        name=BrandArchetypeName.CREATOR,
        data=BrandArchetypeData(
            base_human_need=(
                "Innovation, self-expression; building something of lasting value."
            ),
            archetype_description=(
                "Empowers people to imagine, design, and ship their vision. Provides "
                "tools, frameworks, and communities that turn ideas into finished work."
            ),
            identification_clues=(
                "User creations, templates, toolkits, tutorials. Highlights "
                "customization/versioning/craft; community galleries and challenges."
            ),
            core_shared_values=(
                "Originality, craftsmanship, autonomy, curiosity, mastery of tools, "
                "iteration."
            ),
            typical_target_audience=(
                "Artists, designers, developers, content creators, prosumers/DIY; edu "
                "& prosumer B2B overlap."
            ),
            colors_graphics_description=(
                "Vibrant palettes or refined monochromes; geometric/modular systems. "
                "Display + mono type pairings; UI/component diagrams in visuals."
            ),
            writing_style_description=(
                "Inspiring yet precise; explains how to create great work and why "
                "choices matter. Step-by-step guides and pattern libraries."
            ),
            examples="Adobe, LEGO, Canva",
        ),
    ),
    BrandArchetypeName.RULER: BrandArchetype(
        name=BrandArchetypeName.RULER,
        data=BrandArchetypeData(
            base_human_need=(
                "Control, order, stability, prosperity; reduce uncertainty by setting "
                "standards."
            ),
            archetype_description=(
                "Projects authority and competence; promises world-class quality and "
                "continuity. Leads categories and defines benchmarks—choosing it is "
                "choosing the standard."
            ),
            identification_clues=(
                "Premium codes (metals/crests/seals), endorsements, heritage timelines, "
                "mastery language ('since 19xx,' 'the benchmark'). Immaculate "
                "production."
            ),
            core_shared_values=(
                "Excellence, responsibility, stewardship, legacy; status via mastery."
            ),
            typical_target_audience=(
                "Executives, luxury buyers, institutional/enterprise decision-makers; "
                "older/higher-income skew."
            ),
            colors_graphics_description=(
                "Gold/navy/black/ivory; balanced grids; restrained motion; elegant "
                "serif/sans pairings. Formal, controlled photography."
            ),
            writing_style_description=(
                "Confident, refined, measured. Leads with provenance, standards, proof "
                "of quality; avoids slang/trend-chasing."
            ),
            examples="Rolex, Mercedes-Benz, Louis Vuitton",
        ),
    ),
    BrandArchetypeName.MAGICIAN: BrandArchetype(
        name=BrandArchetypeName.MAGICIAN,
        data=BrandArchetypeData(
            base_human_need=(
                "Transformation, growth, wonder; making the impossible feel effortless."
            ),
            archetype_description=(
                "Reframes reality via hidden levers—tech, insight, ritual—to create "
                "outsized outcomes. Visionary yet empathetic, guiding a seamless "
                "transformation."
            ),
            identification_clues=(
                "Before/after narratives; 'imagine…' setups; demos that feel like "
                "magic. Frictionless UX and surprise-and-delight micro-interactions."
            ),
            core_shared_values=(
                "Ingenuity, insight, optimism, empathy for the journey, elegance."
            ),
            typical_target_audience=(
                "Experience-driven buyers; wellness/transformation seekers; tech "
                "adopters and innovators (B2C + premium B2B)."
            ),
            colors_graphics_description=(
                "Purples/indigos/deep blues; gradients/glow; ethereal/particle/light "
                "motifs. Sleek typography with subtle motion."
            ),
            writing_style_description=(
                "Visionary and uplifting; paints a future state and bridges to it "
                "clearly. Keeps the 'how' elegant and reassuring."
            ),
            examples="Disney, Apple, Dyson",
        ),
    ),
    BrandArchetypeName.LOVER: BrandArchetype(
        name=BrandArchetypeName.LOVER,
        data=BrandArchetypeData(
            base_human_need=(
                "Intimacy, passion, connection, pleasure; desire to savor life and be "
                "desired."
            ),
            archetype_description=(
                "Elevates the senses and celebrates relationships—romantic, self-care, "
                "or communal. Prioritizes aesthetic detail and emotional resonance over "
                "utility alone."
            ),
            identification_clues=(
                "Sensory language, premium materials, lush imagery, rituals "
                "(unboxing/self-care). Focus on beauty, personalization, intimate "
                "moments."
            ),
            core_shared_values=(
                "Passion, beauty, presence, devotion, self-expression, intentional "
                "indulgence."
            ),
            typical_target_audience=(
                "Fashion/beauty/luxury lifestyle; adults seeking premium "
                "experiences/gifts; urban/prosperous skew."
            ),
            colors_graphics_description=(
                "Reds/blush/jewel tones; soft light; curves and tactile textures. "
                "Elegant serif scripts; delicate motion."
            ),
            writing_style_description=(
                "Evocative, sensual, intimate; metaphor and rhythm; invites the reader "
                "to feel. Avoids dryness or cynicism."
            ),
            examples="Chanel, Victoria's Secret, Godiva",
        ),
    ),
    BrandArchetypeName.CAREGIVER: BrandArchetype(
        name=BrandArchetypeName.CAREGIVER,
        data=BrandArchetypeData(
            base_human_need=(
                "Care, service, protection; desire to nurture and keep others safe."
            ),
            archetype_description=(
                "Centers empathy and service—dependable in moments that matter. Reduces "
                "anxiety, builds community, and elevates wellbeing."
            ),
            identification_clues=(
                "Reassuring imagery (families/helpers), testimonials, helplines, "
                "guarantees. Safety protocols/accreditations; responsive support."
            ),
            core_shared_values=(
                "Compassion, trust, patience, responsibility, generosity, community."
            ),
            typical_target_audience=(
                "Parents/caregivers; educators; healthcare & social-impact audiences; "
                "vulnerable or risk-averse buyers."
            ),
            colors_graphics_description=(
                "Soft blues/greens, warm neutrals; rounded icons; smiling eye-level "
                "photography. Open, friendly typography; gentle motion."
            ),
            writing_style_description=(
                "Warm, patient, calming. Clarifies next steps and support; focuses on "
                "relief/outcomes. Avoids urgency bait or guilt tactics."
            ),
            examples="Johnson & Johnson, UNICEF, Red Cross",
        ),
    ),
    BrandArchetypeName.JESTER: BrandArchetype(
        name=BrandArchetypeName.JESTER,
        data=BrandArchetypeData(
            base_human_need=(
                "Joy, play, spontaneity; live in the moment and lighten the mood."
            ),
            archetype_description=(
                "Entertains and disarms, using humor to create memorability and "
                "community. Breaks tension, pokes fun at conventions, humanizes the "
                "brand."
            ),
            identification_clues=(
                "Unexpected copy twists, memes, playful mascots, Easter eggs. Bright "
                "visuals, surprise interactions, timely cultural references."
            ),
            core_shared_values=(
                "Fun, authenticity, creativity, irreverence toward stuffy norms, shared "
                "laughter."
            ),
            typical_target_audience=(
                "Youthful, socially active audiences; entertainment-leaning segments; "
                "participatory culture fans."
            ),
            colors_graphics_description=(
                "Bright multi-color palettes; bold shapes; cartoonish/illustrated "
                "elements; exaggerated motion. Expressive display type and big type "
                "moments."
            ),
            writing_style_description=(
                "Witty, punchy, self-aware; one-liners, callbacks, comedic timing. "
                "Humor serves clarity (never punches down)."
            ),
            examples="Old Spice, Skittles, Duolingo",
        ),
    ),
    BrandArchetypeName.SAGE: BrandArchetype(
        name=BrandArchetypeName.SAGE,
        data=BrandArchetypeData(
            base_human_need=(
                "Understanding, truth, wisdom; make well-informed decisions."
            ),
            archetype_description=(
                "Teaches and clarifies. Synthesizes complex information into frameworks "
                "so people can act with confidence."
            ),
            identification_clues=(
                "Evidence-forward content (citations/benchmarks), explainers, "
                "whitepapers, FAQs. Calm visuals with diagrams/models; domain experts "
                "as protagonists."
            ),
            core_shared_values=(
                "Learning, objectivity, clarity, intellectual humility, long-term "
                "thinking, open inquiry."
            ),
            typical_target_audience=(
                "Researchers, students, professionals, B2B buyers who value "
                "proof/methodology; higher education/income skew."
            ),
            colors_graphics_description=(
                "Cool blues/neutrals; clean typography; charts/tables/system diagrams. "
                "Motion supports comprehension (progressive disclosure, highlights)."
            ),
            writing_style_description=(
                "Clear, precise, instructive; defines terms, cites sources, avoids "
                "sensationalism. Leads with 'what we know and what it means.'"
            ),
            examples="Google, The Economist, Wikipedia",
        ),
    ),
}
