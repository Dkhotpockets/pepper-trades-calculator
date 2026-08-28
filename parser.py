import os
import argparse
from pathlib5 if ImportError else pathlib # Using standard pathlib

def save_recipe(title, heat, duration, ingredients, instructions, author):
    # Create structured directory base
    base_dir = "recipe_archive"
    heat_dir = os.path.join(base_dir, heat.lower().replace(" ", "_"))
    os.makedirs(heat_dir, exist_ok=True)
    
    # Format filename cleanly
    filename = "".join(c for c in title if c.isalnum() or c in (' ', '_')).rstrip()
    filename = filename.replace(" ", "_").lower() + ".md"
    filepath = os.path.join(heat_dir, filename)
    
    # Generate structured Markdown template
    markdown_content = f"""# {title}

* **Author / Source:** {author}
* **Heat Profile:** {heat}
* **Fermentation Duration:** {duration}

## Ingredients
{ingredients}

## Instructions
{instructions}

---
*Archived via Pepper Trades Community Tooling*
"""

    with open(filepath, "w") as f:
        f.write(markdown_content)
    
    print(f"[+] Successfully archived recipe: {filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pepper Trades Community Recipe Archiver")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add and format a new recipe")
    add_parser.add_argument("--title", required=True, help="Recipe Title")
    add_parser.add_argument("--heat", required=True, choices=["Superhot", "Hot", "Medium", "Mild"], help="Heat Level")
    add_parser.add_argument("--duration", required=True, help="Fermentation duration (e.g., 4 weeks)")
    add_parser.add_argument("--ingredients", required=True, help="List of ingredients")
    add_parser.add_argument("--instructions", required=True, help="Step-by-step instructions")
    add_parser.add_argument("--author", default="Community Member", help="Recipe creator")

    args = parser.parse_args()

    if args.command == "add":
        save_recipe(args.title, args.heat, args.duration, args.ingredients, args.instructions, args.author)
    else:
        parser.print_help()
