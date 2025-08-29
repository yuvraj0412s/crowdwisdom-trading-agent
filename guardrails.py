"""
Guardrails for CrowdWisdomTrading AI Agent
Validation and safety checks for agent outputs
"""
import json
from datetime import datetime
from config import Config, logger

def validate_scraped_data(result):
    try:
        logger.info("Running scraped data validation guardrail")
        data = getattr(result, 'raw', str(result))
        try:
            parsed = json.loads(data) if isinstance(data, str) else data
        except json.JSONDecodeError:
            return False, {
                "error": "Invalid JSON format in scraped data", "code": "JSON_PARSE_ERROR",
                "raw_data": str(data)[:500]
            }
        if not isinstance(parsed, dict):
            return False, {"error": "Scraped data must be a dictionary"}
        missing = [f for f in ['products', 'site'] if f not in parsed]
        if missing:
            return False, {"error": f"Missing fields: {missing}", "data": parsed}
        products = parsed.get('products', [])
        if not isinstance(products, list) or len(products) == 0:
            return False, {"error": "No products found", "site": parsed.get('site', 'unknown')}
        valid_products = [
            {
                "title": str(p.get('title', f'Product {i+1}')),
                "price": str(p.get('price', 'Unknown')),
                "category": str(p.get('category', 'General')),
                "site": str(p.get('site', parsed.get('site', 'unknown'))),
                "confidence_score": float(p.get('confidence_score', 0.5))
            } for i, p in enumerate(products) if isinstance(p, dict) and p.get('title')
        ]
        if not valid_products:
            return False, {"error": "No valid products after validation"}
        return True, {
            "site": parsed.get('site'),
            "products": valid_products,
            "products_count": len(valid_products),
            "validation_passed": True,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error validate_scraped_data: {str(e)}")
        return False, {"error": f"Validation exception: {str(e)}"}

def validate_product_matching(result):
    try:
        logger.info("Product matching validation guardrail")
        data = getattr(result, 'raw', str(result))
        try:
            parsed = json.loads(data) if isinstance(data, str) else data
        except json.JSONDecodeError:
            return False, {"error": "Product matching result is not valid JSON"}
        if not isinstance(parsed, dict):
            return False, {"error": "Must be dictionary"}
        missing = [f for f in ['matched_products', 'total_unique_products'] if f not in parsed]
        if missing:
            return False, {"error": f"Missing fields in product matching: {missing}"}
        matched_products = parsed.get('matched_products', [])
        if not isinstance(matched_products, list):
            return False, {"error": "matched_products must be a list"}
        valid = []
        for match in matched_products:
            if isinstance(match, dict) and 'unified_title' in match and 'products' in match:
                products = match['products']
                avg_conf = sum(p.get('confidence_score', 0.5) for p in products) / len(products) if products else 0.5
                valid.append({
                    "unified_title": match['unified_title'],
                    "products": products,
                    "match_confidence": float(match.get('match_confidence', avg_conf)),
                    "sites": list(set(p.get('site', 'unknown') for p in products))
                })
        if not valid:
            return False, {"error": "No valid product matches found"}
        return True, {
            "matched_products": valid,
            "total_unique_products": len(valid),
            "validation_passed": True,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error validate_product_matching: {str(e)}")
        return False, {"error": f"Validation exception: {str(e)}"}

def validate_csv_output(result):
    try:
        data = getattr(result, 'raw', str(result))
        if "CSV" not in data and "csv" not in data:
            return False, {"error": "No CSV content"}
        columns = ['unified_title', 'price', 'sites', 'confidence']
        if sum(1 for col in columns if col in data) < 2:
            return False, {"error": "CSV missing required columns"}
        if len(data.strip()) < 50:
            return False, {"error": "CSV output too short"}
        return True, {
            "csv_content": data,
            "validation_passed": True,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error validate_csv_output: {str(e)}")
        return False, {"error": f"Validation exception: {str(e)}"}

def validate_general_output(result, agent_name="Unknown"):
    try:
        if result is None or len(str(result).strip()) < 10:
            return False, {"error": f"Output from {agent_name} too short"}
        output_str = str(result)
        if any(ind in output_str.lower() for ind in ['error', 'failed', 'exception', 'traceback']):
            return True, {
                "output": output_str,
                "warning": f"Potential error indicators found",
                "validation_passed": True,
                "timestamp": datetime.now().isoformat()
            }
        return True, {
            "output": output_str,
            "validation_passed": True,
            "agent": agent_name,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error validate_general_output: {str(e)}")
        return False, {"error": f"Validation exception: {str(e)}"}

GUARDRAILS = {
    "validate_scraped_data": validate_scraped_data,
    "validate_product_matching": validate_product_matching,
    "validate_csv_output": validate_csv_output,
    "validate_general_output": validate_general_output
}
