"""
Stock & Index Data Downloader
Downloads weekly historical prices (Jan 2019 - Dec 2025) for:
- 5 Major Global Indexes
- 15 Top Companies (3 per index)
"""

import yfinance as yf
import investpy
import os

# Configuration
START_DATE = "2019-01-01"
END_DATE = "2025-12-31"

# 5 Global Indexes
INDEXES = {
    "SP500": "^GSPC",           # S&P 500 (USA)
    "FTSE100": "^FTSE",         # FTSE 100 (UK)
    "NIFTY50": "^NSEI",         # NIFTY 50 (India)
    "Nikkei225": "^N225",       # Nikkei 225 (Japan)
    "NGX_AllShare": "^NGXASI",  # NGX All Share Index (Nigeria) - Note: may have limited data
}

# Top 3 Companies per Index (12 from yfinance, 3 from investpy = 15 total)
COMPANIES = {
    # S&P 500 (USA)
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    
    # FTSE 100 (UK)
    "AstraZeneca": "AZN.L",
    "HSBC": "HSBA.L",
    "Unilever": "ULVR.L",
    
    # NIFTY 50 (India)
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "HDFC_Bank": "HDFCBANK.NS",
    
    # Nikkei 225 (Japan)
    "Toyota": "7203.T",
    "Sony": "6758.T",
    "SoftBank": "9984.T",
}

# Nigerian stocks (US-listed ADRs where available) - DEPRECATED
# Using investpy for actual Nigerian stocks instead
NIGERIAN_ALTERNATIVES_OLD = {
    "Dangote_Cement_Alt": "DANGY",   # OTC Markets
    "MTN_Group": "MTNOY",            # MTN Group (parent company, OTC)
}

# Nigerian stocks via investpy (exact names from investing.com)
NIGERIAN_STOCKS = [
    'Dangote Cement',    # Symbol: DANGCEM
    'MTN Nigeria',       # Symbol: MTNN
    'Access Bank'        # Symbol: ACCESS
]

NIGERIAN_INDEX = 'NSE All Share'  # Nigerian Stock Exchange All Share Index


def create_folders():
    """Create output folders if they don't exist."""
    os.makedirs("Indexes", exist_ok=True)
    os.makedirs("Companies", exist_ok=True)
    print("✓ Created folders: Indexes/, Companies/")


def download_data(tickers: dict, folder_name: str) -> dict:
    """
    Download weekly historical data for given tickers.
    Returns dict with success/failure status for each ticker.
    """
    results = {"success": [], "failed": []}
    
    for name, ticker in tickers.items():
        print(f"  Downloading {name} ({ticker})...", end=" ")
        try:
            data = yf.download(
                ticker,
                start=START_DATE,
                end=END_DATE,
                interval="1wk",
                progress=False
            )
            
            if data.empty:
                print("⚠ No data available")
                results["failed"].append((name, ticker, "No data"))
                continue
            
            # Save to CSV
            filepath = f"{folder_name}/{name}.csv"
            data.to_csv(filepath)
            rows = len(data)
            print(f"✓ Saved ({rows} weeks)")
            results["success"].append((name, ticker, rows))
            
        except Exception as e:
            print(f"✗ Error: {e}")
            results["failed"].append((name, ticker, str(e)))
    
    return results


def download_nigerian_data() -> dict:
    """
    Download Nigerian stocks and index using investpy.
    Returns dict with success/failure status.
    
    NOTE: investpy may be blocked (403 errors) as it relies on web scraping.
    If this happens, see manual download options in the summary.
    """
    results = {"success": [], "failed": []}
    
    # Download Nigerian stocks
    print("\n🇳🇬 Downloading Nigerian Stocks (via investpy)...")
    print("   Note: investpy may be temporarily blocked by investing.com")
    
    for stock in NIGERIAN_STOCKS:
        print(f"  Downloading {stock}...", end=" ")
        try:
            # Try with stock symbol (from the name mapping)
            symbol_map = {
                'Dangote Cement': 'DANGCEM',
                'MTN Nigeria': 'MTNN',
                'Access Bank': 'ACCESS'
            }
            symbol = symbol_map.get(stock, stock)
            
            df = investpy.get_stock_historical_data(
                stock=symbol,
                country='nigeria',
                from_date='01/01/2019',
                to_date='28/12/2025',
                interval='Weekly'
            )
            
            if df.empty:
                print("⚠ No data available")
                results["failed"].append((stock, "investpy", "No data"))
                continue
            
            # Save to CSV
            file_name = stock.replace(" ", "_") + '_Nigeria.csv'
            filepath = f"Companies/{file_name}"
            df.to_csv(filepath)
            rows = len(df)
            print(f"✓ Saved ({rows} weeks)")
            results["success"].append((stock, "investpy", rows))
            
        except Exception as e:
            error_msg = str(e)
            if "403" in error_msg:
                print(f"✗ Blocked (403) - use manual download")
                results["failed"].append((stock, "investpy", "403 Forbidden - blocked by website"))
            else:
                print(f"✗ Error: {e}")
                results["failed"].append((stock, "investpy", str(e)))
    
    # Download Nigerian Index
    print("\n📊 Downloading Nigerian Index (via investpy)...")
    print(f"  Downloading {NIGERIAN_INDEX}...", end=" ")
    try:
        index_df = investpy.get_index_historical_data(
            index=NIGERIAN_INDEX,
            country='nigeria',
            from_date='01/01/2019',
            to_date='28/12/2025',
            interval='Weekly'
        )
        
        if index_df.empty:
            print("⚠ No data available")
            results["failed"].append((NIGERIAN_INDEX, "investpy", "No data"))
        else:
            filepath = "Indexes/Nigeria_All_Share_Index.csv"
            index_df.to_csv(filepath)
            rows = len(index_df)
            print(f"✓ Saved ({rows} weeks)")
            results["success"].append((NIGERIAN_INDEX, "investpy", rows))
            
    except Exception as e:
        error_msg = str(e)
        if "403" in error_msg:
            print(f"✗ Blocked (403) - use manual download")
            results["failed"].append((NIGERIAN_INDEX, "investpy", "403 Forbidden - blocked by website"))
        else:
            print(f"✗ Error: {e}")
            results["failed"].append((NIGERIAN_INDEX, "investpy", str(e)))
    
    return results


def print_summary(index_results: dict, company_results: dict, nigerian_results: dict = None):
    """Print download summary."""
    print("\n" + "=" * 50)
    print("DOWNLOAD SUMMARY")
    print("=" * 50)
    
    print(f"\n📊 INDEXES: {len(index_results['success'])}/5 successful")
    for name, ticker, rows in index_results["success"]:
        print(f"   ✓ {name}: {rows} weeks of data")
    for name, ticker, error in index_results["failed"]:
        print(f"   ✗ {name}: {error}")
    
    # Count total companies including Nigerian ones
    total_companies = 15
    total_company_success = len(company_results["success"])
    
    # Add Nigerian results if available
    if nigerian_results:
        nigerian_stocks = [s for s in nigerian_results["success"] if "Nigeria All Share" not in s[0]]
        total_company_success += len(nigerian_stocks)
        
        # Add Nigerian index to index count
        nigerian_index = [s for s in nigerian_results["success"] if "Nigeria All Share" in s[0]]
        if nigerian_index:
            print(f"\n🇳� NIGERIAN INDEX:")
            for name, source, rows in nigerian_index:
                print(f"   ✓ {name}: {rows} weeks of data")
    
    print(f"\n�🏢 COMPANIES: {total_company_success}/{total_companies} successful")
    for name, ticker, rows in company_results["success"]:
        print(f"   ✓ {name}: {rows} weeks of data")
    for name, ticker, error in company_results["failed"]:
        print(f"   ✗ {name}: {error}")
    
    # Add Nigerian stocks to summary
    if nigerian_results:
        nigerian_stocks = [s for s in nigerian_results["success"] if "Nigeria All Share" not in s[0]]
        for name, source, rows in nigerian_stocks:
            print(f"   ✓ {name}: {rows} weeks of data")
        
        nigerian_failed = [s for s in nigerian_results["failed"] if "Nigeria All Share" not in s[0]]
        for name, source, error in nigerian_failed:
            print(f"   ✗ {name}: {error}")
    
    # Calculate total files
    total_index_files = len(index_results["success"])
    if nigerian_results:
        total_index_files += len([s for s in nigerian_results["success"] if "Nigeria All Share" in s[0]])
    
    total_files = total_index_files + total_company_success
    expected_total = 20  # 5 indexes + 15 companies
    
    print(f"\n📁 Total files created: {total_files}/{expected_total}")
    print("📂 Location: Indexes/ and Companies/ folders")
    
    # Check for Nigerian data failures
    if nigerian_results:
        nigerian_failed_count = len(nigerian_results["failed"])
        if nigerian_failed_count > 0:
            blocked_count = sum(1 for _, _, err in nigerian_results["failed"] if "403" in err)
            if blocked_count > 0:
                print("\n" + "=" * 50)
                print("⚠️  NIGERIAN DATA BLOCKED")
                print("=" * 50)
                print("investpy is currently blocked by investing.com (403 error).")
                print("\n📋 Manual Download Options:")
                print("\n1. Via Investing.com (Web Interface):")
                print("   • Visit: https://www.investing.com/equities/nigeria")
                print("   • Search for: Dangote Cement (DANGCEM), MTN Nigeria (MTNN), Access Bank (ACCESS)")
                print("   • Click 'Historical Data' → Set weekly, 2019-2025 → Download")
                print("   • For index: https://www.investing.com/indices/nigeria-nse-all-share")
                print("\n2. Via African Markets:")
                print("   • Visit: https://www.african-markets.com/en/stock-markets/ngse")
                print("   • Download historical data for NSE All Share Index")
                print("\n3. Via NGX Website:")
                print("   • Visit: https://ngxgroup.com/")
                print("   • Navigate to Market Data → Historical Data")
                print("\n4. Wait and Retry:")
                print("   • investpy blocks are temporary")
                print("   • Try running this script again in a few hours")
                print("   • Use a VPN if issues persist")


def main():
    print("=" * 50)
    print("STOCK & INDEX DATA DOWNLOADER")
    print(f"Period: {START_DATE} to {END_DATE} (Weekly)")
    print("=" * 50)
    
    # Create output folders
    create_folders()
    
    # Download indexes
    print("\n📊 Downloading 5 Global Indexes...")
    index_results = download_data(INDEXES, "Indexes")
    
    # Download companies
    print("\n🏢 Downloading 15 Companies...")
    company_results = download_data(COMPANIES, "Companies")
    
    # Download Nigerian data using investpy
    nigerian_results = download_nigerian_data()
    
    # Print summary
    print_summary(index_results, company_results, nigerian_results)
    
    print("\n✅ Done! Check the Indexes/ and Companies/ folders.")


if __name__ == "__main__":
    main()
