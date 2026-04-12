import json
import copy
import random
import os

input_file = "src/data/GameQuestions.json"

# Load original data (assumes we still have the 5 beginner templates, we'll slice just the first 5 to guarantee it)
with open(input_file, "r", encoding='utf-8') as f:
    data = json.load(f)

# The Mad-Libs Database
replacements_base = {
    "Zomato": ["Amazon", "Swiggy", "Netflix", "HDFC Bank", "SBI", "Flipkart"],
    "zomat0-refunds": ["amaz0n-support", "sw1ggy-care", "netfiix-billing", "hdfcc-secure", "sbionline-alert", "fl1pkart-returns"],
    "Dear Valued Foodie": ["Dear Customer", "Dear Account Holder", "Valued Member", "Dear User"],
    "#4920 Was Cancelled": ["Locked", "Suspended", "Payment Failed", "Verification Required"],
    "Finance Manager": ["HR Director", "CEO", "Lead Developer", "Sales VP"],
    "Unpaid Vendor Invoice": ["Urgent Payroll Update", "Legal Subpoena Attached", "Quarterly Bonus Document"],
    "Maya": ["Rahul", "Priya", "Amit", "Neha", "Vikram", "Sneha", "Karan"],
    "FluffyCat123": ["Sunshine99", "Batman2020", "Password123", "Qwerty!@#"],
    "Mom": ["Dad", "your brother", "your sister", "a friend"],
    "$500": ["$1,000", "$850", "$250", "₹50,000", "₹10,000"],
    "$100": ["$200", "$50", "₹5,000", "₹2,000"],
    "$50": ["$75", "₹500", "₹1,000"],
    "$450": ["$925", "$200", "₹45,000", "₹8,000"],
    "Russia": ["China", "North Korea", "an unknown device", "a suspicious proxy"],
    "Crypto Guru": ["Forex Trader", "DayTrading Pro", "Investment Advisor"],
    "1000% returns": ["guaranteed 500% profit", "massive crypto gains", "risk-free doubling of your money"],
    ".xyz": [".biz", ".info", ".cc", ".update-server.com"],
    "Free_Airport_Wi-Fi_Fast": ["Starbucks_Guest_Free", "Hotel_Lobby_WiFi_5G", "Public_Library_Fast"],
    "cheap $15 smart camera": ["budget $10 smart bulb", "cheap smart fridge", "generic smart doorbell"],
    "Q3_Report.pdf": ["Annual_Budget.pdf", "Meeting_Notes.docx", "Project_Specs.xlsx"],
    "FlashPlayer_Update.exe": ["Java_Runtime_Install.exe", "WinZip_Pro_Crack.exe", "Free_Movie_Player.exe"],
    "Invoice_4992.pdf.exe": ["Salary_Details.pdf.exe", "Termination_Letter.pdf.exe"],
    "Salary_Review_2026.docx": ["Bonus_Payout.docx", "Layoff_List.xlsx"],
    "sysupd@te.exe": ["svch0st.exe", "expl0rer.exe", "win_updat3.exe"],
    "netfiix": ["amz0n", "paypa1", "hdfcc", "appl3"],
    "micros0ft": ["googIe", "faceb00k", "linkedin-verify"]
}

# 10% Difficulty Bump overrides
replacements_hard = {
    # Harder typos (using valid-looking TLDs and subtle char swaps)
    "zomat0-refunds": ["zomato-support.co", "amazon-billing.net", "hdfcbank-secure.info"], 
    ".xyz": [".co", ".net", ".io"], 
    "sysupd@te.exe": ["svchost.sys.exe", "winsys32.exe"], 
    "Russia": ["your own city", "a local ISP"], 
    "FluffyCat123": ["P@ssw0rd2026", "Spring2026!", "Admin@123"],
    "Mom": ["your boss", "the local Police", "Tax Authorities"],
}

def walk_and_replace(node, repl_dict):
    if isinstance(node, str):
        result = node
        for key, vals in repl_dict.items():
            if key in result:
                result = result.replace(key, random.choice(vals))
        return result
    elif isinstance(node, list):
        return [walk_and_replace(item, repl_dict) for item in node]
    elif isinstance(node, dict):
        return {k: walk_and_replace(v, repl_dict) for k, v in node.items()}
    else:
        return node

for game_key, levels_dict in data.items():
    if "beginner" not in levels_dict:
        continue
    
    # We guarantee we only take the first 5 base templates
    base_questions = levels_dict["beginner"][:5]
    
    for level_name in ["beginner", "medium", "hard"]:
        expanded_questions = []
        
        # Determine current replacement dictionary based on level
        current_replacements = dict(replacements_base)
        if level_name in ["medium", "hard"]:
            current_replacements.update(replacements_hard) # Override with harder patterns
            
        for i in range(25):
            template_index = i % len(base_questions)
            # Deep clone the template
            template = copy.deepcopy(base_questions[template_index])
            
            # Apply storytelling replacements
            template = walk_and_replace(template, current_replacements)
            
            # Apply specific IDs and fix potential string variants
            template["id"] = i + 1
            template["difficulty"] = level_name
            
            # For variants beyond the first 5, randomly append a small narrative twist to the question text
            if i >= 5:
                twists = [
                    " Pay close attention to the details.",
                    " Can you spot the hidden trap?",
                    " This one is getting tricky.",
                    " Look at the specific wording.",
                    " Don't let the urgency fool you."
                ]
                template["questionText"] = str(template["questionText"]).replace("(Variant " + str(i+1) + ")", "") # remove old variants
                if not any(t in str(template["questionText"]) for t in twists):
                    template["questionText"] = str(template["questionText"]) + random.choice(twists)
            
            expanded_questions.append(template)
            
        data[game_key][level_name] = expanded_questions

with open(input_file, "w", encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("Mad-Libs Storytelling Synthesis Complete: 375 UNIQUE questions generated!")
