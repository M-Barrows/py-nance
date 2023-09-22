import polars as pl
import pandas as pd

def compound_interest(p:float,r:float,n:int,t:float=1):
    """
    `p : float`, Initial principal balance in the account
    `r : float`, Growth rate (usually APY) of the investment
    `n : int`, Number of times the investment compounds per year (t)
    `t : float` (optional), Number of cycles the investment will remain untouched. If the investment period is less 
        than 1 year, adjust this accordingly. eg: A monthly compounding investment that is held for 9 months would 
        have <n = 12, t = (9/12)>.

    example:
    >>> compound_interest(20000,0.0425,12,(9/12))
    20646.606281143224
    """
    return p*(1+r/n)**(n*t)

def make_compound_reinvestment_df(p:float,r:float,n:int,t:float=1,n_terms:int=1,percent_reinvest:int=100): 
    """
    `p : float`, Initial principal balance in the account
    `r : float`, Growth rate (usually APY) of the investment
    `n : int`, Number of times the investment compounds per year (t)
    `t : float` (optional), Number of cycles the investment will remain untouched. If the investment period is less 
        than 1 year, adjust this accordingly. eg: A monthly compounding investment that is held for 9 months would 
        have <n = 12, t = (9/12)>.
    `n_terms : int` (optional), Number of times this investment will be renewed - reinvesting some percent (`percent_reinvest`) each time.
    `percent_reinvest : int`, percent (1-100) of the investment that should be reinvested each n_terms 

    Usage examples:
    >>> make_compound_reinvestment_df(20000,0.0425,12,(9/12),3,50)
    shape: (4, 4)
    ┌──────┬────────────────┬───────────────┬──────────────┐
    │ Term ┆ Term_Principal ┆ Term_Interest ┆ Total_Value  │
    │ ---  ┆ ---            ┆ ---           ┆ ---          │
    │ i64  ┆ f64            ┆ f64           ┆ f64          │
    ╞══════╪════════════════╪═══════════════╪══════════════╡
    │ 0    ┆ 20000.0        ┆ 0.0           ┆ 20000.0      │
    │ 1    ┆ 10323.303141   ┆ 646.606281    ┆ 20646.606281 │
    │ 2    ┆ 5328.529387    ┆ 333.755633    ┆ 20980.361914 │
    │ 3    ┆ 2750.401208    ┆ 172.273029    ┆ 21152.634942 │
    └──────┴────────────────┴───────────────┴──────────────┘
    """
    term_principal = [p]
    interest_earned = [0]
    term_interest = [0]
    total_value = [p]
    terms_remaining = n_terms
    while terms_remaining > 0:
        term_interest.append(compound_interest(term_principal[-1],r,n,t)-term_principal[-1])
        interest_earned.append(interest_earned[-1] + term_interest[-1])
        total_value.append(total_value[-1] + term_interest[-1])
        term_principal.append((term_principal[-1] + term_interest[-1]) * (percent_reinvest/100))
        terms_remaining -= 1
    df = pd.DataFrame({'Term':list(range(n_terms+1)), 'Term_Principal':term_principal,"Term_Interest":term_interest,"Total_Interest": interest_earned,"Total_Value":total_value})
    return df
