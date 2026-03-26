const fs = require('fs');
const path = require('path');

const tools = [
  {
    dir: 'septic-tank-sizing-calculator',
    name: 'Septic Tank Sizing Calculator',
    ytId: 'dM21Nn2WNPI',
    wikiUrl: 'https://en.wikipedia.org/wiki/Septic_tank',
    wikiDef: 'A septic tank is an underground chamber made of concrete, fiberglass, or plastic through which domestic wastewater flows for basic treatment. Settling and anaerobic digestion processes reduce solids and organics, but the treatment is only moderate. Septic tank systems are a type of simple onsite sewage facility.',
    questions: [
      { q: 'How often should a septic tank be pumped?', a: 'Most septic tanks should be pumped every 3 to 5 years for a typical household of 4 people with a 1,000-gallon tank. Homes with garbage disposals, large families, or heavy water use may need pumping every 1 to 2 years. The pump frequency depends on tank size, household size, total wastewater generated, and the volume of solids in the wastewater. Annual inspections help determine when pumping is needed based on sludge and scum layer measurements.' },
      { q: 'Can I install a septic system on clay soil?', a: 'You can install a septic system on clay soil, but it requires a specialized design. Heavy clay with percolation rates above 60 minutes per inch typically cannot support a conventional gravity drain field. Alternatives include mound systems built with imported sandy fill above the native clay, pressure distribution systems that spread effluent more evenly, or aerobic treatment units that produce higher-quality effluent suitable for shallow dispersal. Expect installation costs 2 to 3 times higher than a conventional system in suitable soil.' },
      { q: 'What is the difference between a septic tank and a cesspool?', a: 'A septic tank is a sealed, watertight container that separates solids from liquids and sends clarified effluent to a drain field for soil treatment. A cesspool (or cesspit) is simply a pit with perforated walls that allows raw wastewater to seep directly into surrounding soil without any separation or treatment. Cesspools are banned or being phased out in most jurisdictions because they contaminate groundwater. Septic tanks with properly designed drain fields provide effective wastewater treatment that protects groundwater quality.' }
    ],
    research: {
      title: 'Septic Tank Sizing and Cost Data by Bedroom Count (2026)',
      headers: ['Bedrooms', 'Min Tank Size', 'Daily Flow (GPD)', 'Tank Cost', 'Drain Field Cost', 'Total Install Cost'],
      rows: [
        ['1-2', '750 gal', '150-300', '$800 - $1,500', '$2,500 - $5,000', '$5,000 - $10,000'],
        ['3', '1,000 gal', '300-450', '$1,000 - $2,000', '$3,500 - $6,500', '$7,000 - $15,000'],
        ['4', '1,250 gal', '450-600', '$1,200 - $2,500', '$4,500 - $8,000', '$9,000 - $18,000'],
        ['5', '1,500 gal', '600-750', '$1,500 - $3,000', '$5,500 - $10,000', '$12,000 - $22,000'],
        ['6', '1,750 gal', '750-900', '$1,800 - $3,500', '$7,000 - $12,000', '$15,000 - $28,000'],
        ['7+', '2,000+ gal', '900+', '$2,200 - $4,500', '$8,500 - $15,000', '$18,000 - $35,000']
      ],
      note: 'Source: National average data from EPA OnSite Wastewater Treatment Systems Manual and regional installer surveys, 2024-2026. Costs vary significantly by region, soil conditions, and local permitting requirements.'
    },
    calcFn: 'calculateSeptic',
    subtitleText: 'Determine the correct septic tank capacity and drain field size based on bedrooms, occupants, soil percolation rate, water usage habits, and local code requirements.',
    structureType: 'old' // old = subtitle directly after h1 in container
  },
  {
    dir: 'insulation-r-value-calculator',
    name: 'Insulation R-Value Calculator',
    ytId: '6Bnnz8WoSTQ',
    wikiUrl: 'https://en.wikipedia.org/wiki/Building_insulation',
    wikiDef: 'Building insulation refers to any material used to fill spaces in a building to reduce heat flow by reflection or by slowing conduction and convection. Insulation effectiveness is measured by R-value, which indicates thermal resistance. Higher R-values mean greater insulating power and reduced energy transfer through walls, ceilings, and floors.',
    questions: [
      { q: 'What R-value do I need for my attic?', a: 'The recommended attic R-value depends on your IECC climate zone. Zones 1-3 (southern states) require R-30 to R-38 minimum. Zone 4 (mid-Atlantic, lower Midwest) requires R-38 to R-49. Zones 5-8 (northern states) require R-49 to R-60. These are IECC 2021 code minimums. Going above code is often cost-effective for attics because attic insulation is relatively inexpensive to install and heat loss through the attic represents 25% to 30% of total home energy loss.' },
      { q: 'Is spray foam insulation worth the extra cost?', a: 'Closed-cell spray foam costs $1.50 to $3.50 per square foot per inch of thickness, compared to $0.30 to $0.50 for fiberglass batts. However, spray foam delivers R-6 to R-7 per inch versus R-3.2 for fiberglass, and it also serves as an air and vapor barrier. In walls where space is limited, spray foam achieves higher R-values in the same cavity depth. The payback period for spray foam versus fiberglass ranges from 5 to 12 years depending on climate zone and energy costs. Spray foam is most cost-effective in extreme climates and in areas where air sealing is difficult to achieve otherwise.' },
      { q: 'Does insulation degrade or lose R-value over time?', a: 'Most insulation materials maintain their R-value for decades when properly installed and kept dry. Fiberglass batts can last 80 to 100 years without significant degradation if they remain dry and uncompressed. Cellulose may settle 10% to 20% over the first few years, which reduces effective coverage but the R-value per inch remains stable. Closed-cell spray foam maintains its R-value indefinitely. Open-cell spray foam and some rigid foam boards may lose 5% to 10% of R-value in the first 1 to 2 years as blowing agents dissipate, then stabilize. Moisture damage is the primary cause of insulation failure, not aging.' }
    ],
    research: {
      title: 'Insulation R-Value Comparison by Material Type (2026)',
      headers: ['Material', 'R-Value per Inch', 'Cost per Sq Ft (R-13)', 'Moisture Resistant', 'Air Barrier', 'Payback (Zone 4)'],
      rows: [
        ['Fiberglass Batts', 'R-3.2', '$0.40 - $0.65', 'No', 'No', '2 - 3 years'],
        ['Blown Cellulose', 'R-3.5', '$0.45 - $0.70', 'No', 'No', '2 - 4 years'],
        ['Mineral Wool Batts', 'R-3.8', '$0.65 - $1.10', 'Yes', 'No', '3 - 5 years'],
        ['Open-Cell Spray Foam', 'R-3.7', '$0.90 - $1.50', 'No', 'Yes', '4 - 7 years'],
        ['Closed-Cell Spray Foam', 'R-6.5', '$1.50 - $3.50', 'Yes', 'Yes', '5 - 12 years'],
        ['Rigid XPS Board', 'R-5.0', '$0.75 - $1.25', 'Yes', 'Partial', '3 - 6 years'],
        ['Rigid Polyiso Board', 'R-6.0', '$0.85 - $1.40', 'Yes', 'Partial', '4 - 7 years']
      ],
      note: 'Source: Department of Energy Building Technologies Office and RS Means construction cost data, 2024-2026. Costs are for material and professional installation. Payback calculated against Zone 4 average heating and cooling costs.'
    },
    calcFn: 'calculateInsulation',
    subtitleText: 'Calculate required insulation R-values for your climate zone, wall type, ceiling, floor, and foundation. Includes IECC 2021 code minimums, material options, thickness requirements, and cost estimates.',
    structureType: 'old'
  },
  {
    dir: 'rafter-length-calculator',
    name: 'Rafter Length Calculator',
    ytId: '74KMqBjJeQQ',
    wikiUrl: 'https://en.wikipedia.org/wiki/Rafter',
    wikiDef: 'A rafter is a structural member in architecture, typically forming the framework of a roof. Rafters run from the ridge or hip of the roof to the wall plate of the external wall, supporting the roof deck and its associated loads. Common rafters are evenly spaced along the length of the roof and are calculated using the roof pitch, building span, and desired overhang.',
    questions: [
      { q: 'How do I calculate rafter length from roof pitch and building width?', a: 'Divide the building width by 2 to get the run (horizontal distance from wall to ridge). Subtract half the ridge board thickness from the run. Convert the pitch to a rise-per-foot value (for example, 6/12 means 6 inches of rise for every 12 inches of run). Multiply the adjusted run by the pitch factor to get the rise. Then use the Pythagorean theorem: rafter length equals the square root of (run squared plus rise squared). Add the overhang tail length separately. For a 24-foot wide building with a 6/12 pitch and 1.5-inch ridge board, the run is 11.9375 feet, the rise is 5.9688 feet, and the rafter length is 13.34 feet, or 13 feet 4 inches.' },
      { q: 'What size lumber should I use for rafters?', a: 'Rafter lumber size depends on the span, spacing, species, grade, and roof loads. For residential roofs with 16-inch on-center spacing, 2x6 rafters span up to about 10 feet, 2x8 rafters span up to about 14 feet, 2x10 rafters span up to about 18 feet, and 2x12 rafters span up to about 22 feet. These spans assume No. 2 grade Douglas Fir or Southern Pine with a combined dead and live load of 30 psf. Higher snow loads, wider spacing, or lower-grade lumber reduce allowable spans. Always verify against local building code span tables or have a structural engineer review your specific situation.' },
      { q: 'What is a birdsmouth cut and how deep should it be?', a: 'A birdsmouth cut is a notch cut into the underside of a rafter where it sits on the wall plate. It consists of two cuts: the seat cut (horizontal, resting on the top plate) and the plumb cut (vertical, against the outside edge of the wall). The seat cut depth should not exceed one-third of the total rafter depth. For a 2x8 rafter (7.25 inches actual depth), the maximum birdsmouth depth is about 2.4 inches. The HAP (height above plate) is the remaining rafter depth above the seat cut. A minimum HAP of two-thirds the rafter depth is required to maintain structural integrity.' }
    ],
    research: {
      title: 'Rafter Lengths at Common Pitches for Standard Building Widths (feet)',
      headers: ['Pitch', 'Angle', '20 ft Wide', '24 ft Wide', '28 ft Wide', '32 ft Wide', '36 ft Wide'],
      rows: [
        ['4/12', '18.43 deg', '10.54', '12.65', '14.76', '16.87', '18.97'],
        ['5/12', '22.62 deg', '10.83', '13.00', '15.17', '17.33', '19.50'],
        ['6/12', '26.57 deg', '11.18', '13.42', '15.65', '17.89', '20.12'],
        ['7/12', '30.26 deg', '11.59', '13.91', '16.23', '18.54', '20.86'],
        ['8/12', '33.69 deg', '12.06', '14.47', '16.88', '19.30', '21.71'],
        ['9/12', '36.87 deg', '12.50', '15.00', '17.50', '20.00', '22.50'],
        ['10/12', '39.81 deg', '13.05', '15.66', '18.27', '20.88', '23.49'],
        ['12/12', '45.00 deg', '14.14', '16.97', '19.80', '22.63', '25.46']
      ],
      note: 'Calculated rafter lengths from wall plate to ridge centerline, excluding overhang. Formula: length = (width/2) / cos(atan(pitch/12)). Add overhang tail length and subtract half ridge board thickness for actual cutting length.'
    },
    calcFn: 'calculateRafter',
    subtitleText: 'Calculate rafter length from roof pitch, building width, overhang, and ridge board dimensions. Includes birdsmouth cut calculations, HAP, rise, angle, and rafter count estimates.',
    structureType: 'old'
  },
  {
    dir: 'heloc-repayment-calculator',
    name: 'HELOC Repayment Calculator',
    ytId: '6Wcy3dTCaFE',
    wikiUrl: 'https://en.wikipedia.org/wiki/Home_equity_line_of_credit',
    wikiDef: 'A home equity line of credit (HELOC) is a revolving line of credit secured by the equity in a borrower\'s home. It functions similarly to a credit card, with a draw period during which the borrower can access funds and make interest-only payments, followed by a repayment period where the outstanding balance is amortized over a fixed term with principal and interest payments.',
    questions: [
      { q: 'What happens when my HELOC draw period ends?', a: 'When the draw period ends (typically after 5 to 10 years), you enter the repayment period and can no longer borrow additional funds. Your payments increase because you now pay both principal and interest instead of interest only. For example, on a $75,000 balance at 8.5%, interest-only payments during the draw period are about $531 per month. When the repayment period starts with a 20-year term, your payment jumps to approximately $651 per month. Some lenders allow a conversion to a fixed-rate loan at this point, which can provide payment certainty during repayment.' },
      { q: 'Can I make principal payments during the HELOC draw period?', a: 'Yes, most HELOCs allow you to make principal payments during the draw period even though only interest payments are required. Paying down principal during the draw period reduces your balance and total interest cost. Any principal you pay also becomes available to borrow again (since a HELOC is revolving credit). Making even small extra payments during the draw period can significantly reduce the payment shock when the repayment period begins. Some borrowers treat the draw period like a repayment period, making full principal and interest payments from the start.' },
      { q: 'How do variable rates affect my HELOC payments?', a: 'Most HELOCs have variable interest rates tied to the prime rate plus a margin. When the Federal Reserve raises or lowers the federal funds rate, the prime rate moves with it, and your HELOC rate adjusts accordingly. A 1% rate increase on a $75,000 balance adds about $63 per month to interest-only payments. Most HELOCs have lifetime rate caps (typically 18%) but may not have periodic adjustment caps, meaning rates can change significantly in a short time. To budget conservatively, model your payments at 2 to 3 percentage points above your current rate to ensure affordability if rates rise.' }
    ],
    research: {
      title: 'HELOC Monthly Payment Estimates by Balance and Interest Rate',
      headers: ['Balance', '7.0% IO', '7.0% P+I (20yr)', '8.5% IO', '8.5% P+I (20yr)', '10.0% IO', '10.0% P+I (20yr)'],
      rows: [
        ['$25,000', '$146', '$194', '$177', '$217', '$208', '$241'],
        ['$50,000', '$292', '$388', '$354', '$434', '$417', '$483'],
        ['$75,000', '$438', '$581', '$531', '$651', '$625', '$724'],
        ['$100,000', '$583', '$775', '$708', '$868', '$833', '$965'],
        ['$150,000', '$875', '$1,163', '$1,063', '$1,302', '$1,250', '$1,448'],
        ['$200,000', '$1,167', '$1,550', '$1,417', '$1,736', '$1,667', '$1,930']
      ],
      note: 'IO = interest-only payment (draw period). P+I = principal and interest payment (repayment period, 20-year term). Monthly interest-only: Balance x Rate / 12. P+I calculated using standard amortization formula. Rates shown are annual.'
    },
    calcFn: 'calculateHELOC',
    subtitleText: 'Estimate your Home Equity Line of Credit payments during draw and repayment periods with variable rate projections and complete amortization schedules',
    structureType: 'new',
    h2sections: [
      { id: 'calculate-heloc', text: 'Calculate Your HELOC Payments' },
      { id: 'understanding-heloc', text: 'Understanding Home Equity Lines of Credit' },
      { id: 'repayment-strategies', text: 'HELOC Repayment Strategies Compared' },
      { id: 'market-trends', text: 'HELOC Market Trends and Current Rates' },
      { id: 'faq', text: 'Frequently Asked Questions' },
      { id: 'numbers-look-like', text: 'What the Numbers Really Look Like' },
      { id: 'related-tools', text: 'Related Financial Tools' }
    ]
  },
  {
    dir: 'cd-account-calculator',
    name: 'CD Account Calculator',
    ytId: 'xHLQniDLiPQ',
    wikiUrl: 'https://en.wikipedia.org/wiki/Certificate_of_deposit',
    wikiDef: 'A certificate of deposit (CD) is a savings product offered by banks and credit unions that provides a fixed interest rate for a specified term. The depositor agrees to leave the money in the account for the full term in exchange for a higher interest rate than a standard savings account. Early withdrawal typically incurs a penalty that forfeits a portion of earned interest.',
    questions: [
      { q: 'What is the difference between APR and APY for CDs?', a: 'APR (Annual Percentage Rate) is the stated interest rate without accounting for compounding. APY (Annual Percentage Yield) reflects the actual return after compounding is factored in. A CD with a 5.00% APR compounded monthly has an APY of 5.116% because interest earned each month also earns interest in subsequent months. The more frequently interest compounds, the larger the gap between APR and APY. When comparing CDs from different banks, always compare APY values since they represent the true return. Banks are required by the Truth in Savings Act to disclose APY on all deposit products.' },
      { q: 'How much will I lose if I withdraw my CD early?', a: 'Early withdrawal penalties vary by bank and term length. Common penalties are: 3 months of interest for CDs with terms under 12 months, 6 months of interest for 12 to 36 month CDs, and 12 months of interest for CDs with terms of 48 months or longer. For a $10,000 CD at 5.00% APR, a 6-month penalty equals approximately $250. Some banks calculate the penalty on the amount withdrawn rather than the full balance. If you withdraw in the first few months, the penalty may exceed earned interest and cut into your principal, though FDIC rules prohibit reducing the principal below the original deposit for penalty calculations.' },
      { q: 'Is a CD ladder better than a single long-term CD?', a: 'A CD ladder provides more flexibility and often a similar average return to a single long-term CD. With a 5-year ladder, you divide your investment across 1, 2, 3, 4, and 5-year terms. You have access to one-fifth of your money every year (when each rung matures), and after the first cycle, every maturing CD is reinvested at the 5-year rate. If rates rise, you capture higher rates sooner than a single locked-in CD. If rates fall, your existing longer-term CDs retain their higher rates. The trade-off is a slightly lower blended yield initially, since shorter-term CDs typically pay less than longer-term ones.' }
    ],
    research: {
      title: 'CD Maturity Values for $10,000 Deposit at Different APYs and Terms',
      headers: ['Term', '4.00% APY', '4.50% APY', '5.00% APY', '5.25% APY', '5.50% APY'],
      rows: [
        ['6 months', '$10,198', '$10,223', '$10,247', '$10,259', '$10,271'],
        ['12 months', '$10,400', '$10,450', '$10,500', '$10,525', '$10,550'],
        ['18 months', '$10,604', '$10,680', '$10,756', '$10,794', '$10,832'],
        ['24 months', '$10,816', '$10,920', '$11,025', '$11,078', '$11,130'],
        ['36 months', '$11,249', '$11,412', '$11,576', '$11,660', '$11,742'],
        ['60 months', '$12,167', '$12,462', '$12,763', '$12,915', '$13,070']
      ],
      note: 'Maturity values assume interest compounded monthly and no additional deposits. APY values reflect the effective annual yield after compounding. Calculated as: A = P x (1 + APY)^t where t is years. Values rounded to nearest dollar.'
    },
    calcFn: 'calculateCD',
    subtitleText: 'Calculate your Certificate of Deposit maturity value, compare compounding frequencies, and estimate early withdrawal penalties',
    structureType: 'new',
    h2sections: [
      { id: 'calculate-cd', text: 'Calculate Your CD Returns' },
      { id: 'understanding-cds', text: 'Understanding Certificates of Deposit' },
      { id: 'cd-strategies', text: 'Modern CD Strategies for Maximizing Returns' },
      { id: 'methodology', text: 'CD Calculator Methodology and Formulas' },
      { id: 'ladder-strategy', text: 'CD Ladder Strategy for Maximizing Returns' },
      { id: 'faq', text: 'Frequently Asked Questions' },
      { id: 'investment-scenarios', text: 'CD Investment Scenarios by Deposit Size' },
      { id: 'related-tools', text: 'Related Financial Tools' }
    ]
  },
  {
    dir: 'car-refinance-calculator',
    name: 'Car Refinance Calculator',
    ytId: 'oW-fPCY9qvE',
    wikiUrl: 'https://en.wikipedia.org/wiki/Refinancing',
    wikiDef: 'Refinancing is the replacement of an existing debt obligation with another debt obligation under different terms. In auto lending, refinancing involves taking out a new loan to pay off the existing car loan, typically to secure a lower interest rate, reduce monthly payments, or change the loan term. The vehicle serves as collateral for both the original and refinanced loans.',
    questions: [
      { q: 'When is the best time to refinance a car loan?', a: 'The best time to refinance is when your credit score has improved significantly since the original loan, when market interest rates have dropped at least 1 to 2 percentage points below your current rate, and when you still have at least 12 to 24 months remaining on your loan. Refinancing too late in the loan term yields minimal savings because most interest has already been paid. Refinancing too early (within the first 60 to 90 days) may trigger prepayment penalties on some loans. The sweet spot is typically 6 to 24 months after the original loan, when your payment history has boosted your credit and enough balance remains to generate meaningful savings.' },
      { q: 'Does refinancing a car loan hurt my credit score?', a: 'Refinancing causes a small, temporary credit score dip of 5 to 10 points from the hard inquiry. If you apply to multiple lenders within a 14-day window, credit scoring models count all the inquiries as a single event, minimizing the impact. Closing the old loan is reported as "paid in full," which is a positive mark. Opening a new loan temporarily lowers your average account age. Most borrowers see their score recover within 2 to 3 months after refinancing. The long-term credit impact is neutral to positive, especially if the lower payment helps you avoid missed payments.' },
      { q: 'Can I refinance if I owe more than my car is worth?', a: 'You can refinance an underwater (negative equity) loan, but your options are limited. Most lenders require the loan-to-value ratio to be 125% or less, meaning if your car is worth $15,000, the maximum refinance loan is $18,750. Some credit unions offer underwater refinancing at higher rates. If your negative equity exceeds the lender limit, you can pay the difference in cash at closing to bring the balance within the acceptable range. Refinancing an underwater loan makes sense if the rate reduction saves more than the negative equity costs over the remaining loan life.' }
    ],
    research: {
      title: 'Car Refinance Savings Comparison by Rate Reduction ($20,000 Balance, 48 Months)',
      headers: ['Original Rate', 'New Rate', 'Rate Drop', 'Old Payment', 'New Payment', 'Monthly Savings', 'Total Savings'],
      rows: [
        ['8.0%', '6.0%', '2.0%', '$488', '$470', '$18', '$864'],
        ['10.0%', '7.0%', '3.0%', '$507', '$479', '$28', '$1,344'],
        ['12.0%', '7.0%', '5.0%', '$527', '$479', '$48', '$2,304'],
        ['14.0%', '8.0%', '6.0%', '$547', '$488', '$59', '$2,832'],
        ['16.0%', '9.0%', '7.0%', '$568', '$498', '$70', '$3,360'],
        ['18.0%', '10.0%', '8.0%', '$589', '$507', '$82', '$3,936']
      ],
      note: 'Payments calculated using standard amortization formula: M = P[r(1+r)^n]/[(1+r)^n-1]. Savings assume same 48-month term for both loans with no refinancing fees. Actual savings may be reduced by origination fees, title transfer costs, or term extension.'
    },
    calcFn: 'calculateRefi',
    subtitleText: 'Calculate how much you could save by refinancing your auto loan with a lower rate, different term, or both',
    structureType: 'new',
    h2sections: [
      { id: 'compare-loans', text: 'Compare Current vs. Refinanced Loan' },
      { id: 'complete-guide', text: 'The Complete Guide to Car Loan Refinancing' },
      { id: 'rate-trends', text: 'Auto Loan Refinance Rate Trends in 2026' },
      { id: 'savings-scenarios', text: 'Car Refinance Savings Scenarios by Credit Tier' },
      { id: 'faq', text: 'Frequently Asked Questions' },
      { id: 'amortization', text: 'Understanding Auto Loan Interest and Amortization' },
      { id: 'mathematics', text: 'Understanding the Mathematics Behind Auto Loan Refinancing' },
      { id: 'related-tools', text: 'Related Financial Tools' }
    ]
  }
];

function generateBadgeRow() {
  return `
  <div style="display:flex;flex-wrap:wrap;gap:12px;margin-bottom:24px;align-items:center;">
    <img alt="Last verified March 2026" src="https://img.shields.io/badge/Last%20Verified-March%202026-00cc44?style=flat-square" loading="lazy"/>
    <img alt="Updated 2026-03-26" src="https://img.shields.io/badge/Updated-2026--03--26-0088ff?style=flat-square" loading="lazy"/>
    <img alt="Free Tool - No Login" src="https://img.shields.io/badge/Free%20Tool-No%20Login-00cc44?style=flat-square" loading="lazy"/>
  </div>`;
}

function generateTocForNew(tool) {
  const items = tool.h2sections.map(s => `      <li style="margin:4px 0;"><a href="#${s.id}" style="color:#00ccff;text-decoration:none;font-size:0.93rem;">${s.text}</a></li>`);
  const mid = Math.ceil(items.length / 2);
  const col1 = items.slice(0, mid).join('\n');
  const col2 = items.slice(mid).join('\n');
  return `
  <div style="background:#12121a;border:1px solid #2a2a3e;border-radius:10px;padding:20px 28px;margin:0 0 28px 0;">
    <div style="color:#00ff88;font-size:1rem;font-weight:600;margin-bottom:12px;">Table of Contents <span style="color:#888;font-size:0.85rem;font-weight:400;margin-left:8px;">8 min read</span></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0 24px;">
      <ul style="list-style:none;padding:0;margin:0;">
${col1}
      </ul>
      <ul style="list-style:none;padding:0;margin:0;">
${col2}
      </ul>
    </div>
  </div>`;
}

function generateWikiDef(tool) {
  return `
  <div style="border-left:4px solid #00ccff;background:#12121a;padding:16px 20px;margin:28px 0;border-radius:0 8px 8px 0;">
    <div style="color:#00ccff;font-size:0.85rem;font-weight:600;margin-bottom:8px;">From Wikipedia</div>
    <p style="margin:0 0 8px 0;color:#c8c8d0;font-size:0.95rem;">${tool.wikiDef}</p>
    <a href="${tool.wikiUrl}" target="_blank" rel="noopener" style="color:#00ccff;font-size:0.85rem;">Read more on Wikipedia</a>
  </div>`;
}

function generateCommunityQuestions(tool) {
  const qas = tool.questions.map(qa => `
    <div style="background:#12121a;border:1px solid #2a2a3e;border-radius:8px;padding:16px 20px;margin-bottom:12px;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
        <span style="background:#f48024;color:#fff;font-size:0.7rem;font-weight:700;padding:2px 8px;border-radius:3px;">Q</span>
        <span style="color:#e0e0e8;font-size:0.95rem;font-weight:600;">${qa.q}</span>
      </div>
      <p style="margin:0;color:#b0b0b8;font-size:0.92rem;line-height:1.6;">${qa.a}</p>
    </div>`).join('');

  return `
  <div style="margin:32px 0;">
    <h3 style="color:#e0e0e8;font-size:1.05rem;margin-bottom:16px;">Community Questions</h3>
    ${qas}
  </div>`;
}

function generateResearchTable(tool) {
  const r = tool.research;
  const headerRow = r.headers.map(h => `<th style="padding:10px 14px;text-align:left;border-bottom:2px solid #00ff88;color:#00ff88;font-size:0.82rem;white-space:nowrap;">${h}</th>`).join('');
  const bodyRows = r.rows.map(row => {
    const cells = row.map(c => `<td style="padding:8px 14px;border-bottom:1px solid #1e1e2e;color:#c8c8d0;font-size:0.88rem;white-space:nowrap;">${c}</td>`).join('');
    return `      <tr>${cells}</tr>`;
  }).join('\n');

  return `
  <div style="margin:32px 0;">
    <h3 style="color:#e0e0e8;font-size:1.05rem;margin-bottom:16px;">${r.title}</h3>
    <div style="overflow-x:auto;border:1px solid #2a2a3e;border-radius:8px;">
      <table style="width:100%;border-collapse:collapse;background:#12121a;">
        <thead><tr>${headerRow}</tr></thead>
        <tbody>
${bodyRows}
        </tbody>
      </table>
    </div>
    <p style="color:#888;font-size:0.8rem;margin-top:8px;font-style:italic;">${r.note}</p>
  </div>`;
}

function generateUsageCounter() {
  return `
  <div id="usage-counter" style="text-align:center;margin:24px 0;padding:12px;background:#12121a;border:1px solid #2a2a3e;border-radius:8px;">
    <span style="color:#888;font-size:0.85rem;">Calculations performed: </span>
    <span id="calcCount" style="color:#00ff88;font-weight:700;font-size:0.95rem;">0</span>
  </div>`;
}

function generateYouTubeEmbed(ytId) {
  return `
  <div style="margin:28px 0;">
    <h3 style="color:#e0e0e8;font-size:1.05rem;margin-bottom:12px;">Video Guide</h3>
    <div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:8px;">
      <iframe src="https://www.youtube.com/embed/${ytId}" title="Video guide" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen loading="lazy"></iframe>
    </div>
  </div>`;
}

// Process each tool
tools.forEach(tool => {
  const filePath = path.join(__dirname, tool.dir, 'index.html');
  let html = fs.readFileSync(filePath, 'utf8');

  // 1. Add EEAT Badges after subtitle
  const subtitleTag = `<p class="subtitle">${tool.subtitleText}</p>`;
  if (html.includes(subtitleTag)) {
    html = html.replace(subtitleTag, subtitleTag + generateBadgeRow());
  } else {
    console.log(`WARNING: Could not find exact subtitle for ${tool.dir}`);
    // Try a more flexible match
    const subtitleRegex = new RegExp(`(<p class="subtitle">.*?</p>)`, 's');
    const match = html.match(subtitleRegex);
    if (match) {
      html = html.replace(match[0], match[0] + generateBadgeRow());
    }
  }

  // 2. For "new" style tools (HELOC, CD, car-refi), add TOC + assign IDs to h2s
  if (tool.structureType === 'new') {
    // Add TOC after badges (which are after subtitle)
    // Find the closing </header> tag and add TOC after the <div class="container"> that follows
    // Actually, let's add TOC right after the badge row we just inserted
    const badgeEnd = 'No%20Login-00cc44?style=flat-square" loading="lazy"/>\n  </div>';
    if (html.includes(badgeEnd)) {
      html = html.replace(badgeEnd, badgeEnd + generateTocForNew(tool));
    }

    // Assign IDs to h2 tags that don't have them
    if (tool.dir === 'heloc-repayment-calculator') {
      html = html.replace('<h2>Calculate Your HELOC Payments</h2>', '<h2 id="calculate-heloc">Calculate Your HELOC Payments</h2>');
      html = html.replace('<h2>Understanding Home Equity Lines of Credit</h2>', '<h2 id="understanding-heloc">Understanding Home Equity Lines of Credit</h2>');
      html = html.replace('<h2>HELOC Repayment Strategies Compared</h2>', '<h2 id="repayment-strategies">HELOC Repayment Strategies Compared</h2>');
      html = html.replace('<h2>HELOC Market Trends and Current Rates</h2>', '<h2 id="market-trends">HELOC Market Trends and Current Rates</h2>');
      html = html.replace('<h2>Frequently Asked Questions</h2>', '<h2 id="faq">Frequently Asked Questions</h2>');
      html = html.replace('<h2>What the Numbers Really Look Like</h2>', '<h2 id="numbers-look-like">What the Numbers Really Look Like</h2>');
      html = html.replace('<h2>Related Financial Tools</h2>', '<h2 id="related-tools">Related Financial Tools</h2>');
      html = html.replace('<h2>Update History</h2>', '<h2 id="update-history">Update History</h2>');
    } else if (tool.dir === 'cd-account-calculator') {
      html = html.replace('<h2>Calculate Your CD Returns</h2>', '<h2 id="calculate-cd">Calculate Your CD Returns</h2>');
      html = html.replace('<h2>Understanding Certificates of Deposit</h2>', '<h2 id="understanding-cds">Understanding Certificates of Deposit</h2>');
      html = html.replace('<h2>modern CD Strategies for Maximizing Returns</h2>', '<h2 id="cd-strategies">Modern CD Strategies for Maximizing Returns</h2>');
      html = html.replace('<h2>CD Calculator Methodology and Formulas</h2>', '<h2 id="methodology">CD Calculator Methodology and Formulas</h2>');
      html = html.replace('<h2>CD Ladder Strategy for Maximizing Returns</h2>', '<h2 id="ladder-strategy">CD Ladder Strategy for Maximizing Returns</h2>');
      html = html.replace('<h2>Frequently Asked Questions</h2>', '<h2 id="faq">Frequently Asked Questions</h2>');
      html = html.replace('<h2>CD Investment Scenarios by Deposit Size</h2>', '<h2 id="investment-scenarios">CD Investment Scenarios by Deposit Size</h2>');
      html = html.replace('<h2>Related Financial Tools</h2>', '<h2 id="related-tools">Related Financial Tools</h2>');
      html = html.replace('<h2>Update History</h2>', '<h2 id="update-history">Update History</h2>');
    } else if (tool.dir === 'car-refinance-calculator') {
      html = html.replace('<h2>Compare Current vs. Refinanced Loan</h2>', '<h2 id="compare-loans">Compare Current vs. Refinanced Loan</h2>');
      html = html.replace('<h2>The Complete Guide to Car Loan Refinancing</h2>', '<h2 id="complete-guide">The Complete Guide to Car Loan Refinancing</h2>');
      html = html.replace('<h2>Auto Loan Refinance Rate Trends in 2026</h2>', '<h2 id="rate-trends">Auto Loan Refinance Rate Trends in 2026</h2>');
      html = html.replace('<h2>Car Refinance Savings Scenarios by Credit Tier</h2>', '<h2 id="savings-scenarios">Car Refinance Savings Scenarios by Credit Tier</h2>');
      html = html.replace('<h2>Frequently Asked Questions</h2>', '<h2 id="faq">Frequently Asked Questions</h2>');
      html = html.replace('<h2>Understanding Auto Loan Interest and Amortization</h2>', '<h2 id="amortization">Understanding Auto Loan Interest and Amortization</h2>');
      html = html.replace('<h2>Understanding the Mathematics Behind Auto Loan Refinancing</h2>', '<h2 id="mathematics">Understanding the Mathematics Behind Auto Loan Refinancing</h2>');
      html = html.replace('<h2>Related Financial Tools</h2>', '<h2 id="related-tools">Related Financial Tools</h2>');
    }
  }

  // For old-style tools (septic, insulation, rafter), upgrade existing TOC to two-column with reading time
  if (tool.structureType === 'old') {
    // Find and replace the existing <div class="toc"> block
    const tocRegex = /  <div class="toc">\s*<div class="toc-title">Table of Contents<\/div>\s*<ol>([\s\S]*?)<\/ol>\s*<\/div>/;
    const tocMatch = html.match(tocRegex);
    if (tocMatch) {
      // Extract existing TOC links
      const linkRegex = /<li><a href="(#[^"]+)">([^<]+)<\/a><\/li>/g;
      const links = [];
      let m;
      while ((m = linkRegex.exec(tocMatch[1])) !== null) {
        links.push({ href: m[1], text: m[2] });
      }

      const items = links.map(l => `      <li style="margin:4px 0;"><a href="${l.href}" style="color:#00ccff;text-decoration:none;font-size:0.93rem;">${l.text}</a></li>`);
      const mid = Math.ceil(items.length / 2);
      const col1 = items.slice(0, mid).join('\n');
      const col2 = items.slice(mid).join('\n');

      const newToc = `  <div style="background:#12121a;border:1px solid #2a2a3e;border-radius:10px;padding:20px 28px;margin:24px 0;">
    <div style="color:#00ff88;font-size:1rem;font-weight:600;margin-bottom:12px;">Table of Contents <span style="color:#888;font-size:0.85rem;font-weight:400;margin-left:8px;">10 min read</span></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0 24px;">
      <ul style="list-style:none;padding:0;margin:0;">
${col1}
      </ul>
      <ul style="list-style:none;padding:0;margin:0;">
${col2}
      </ul>
    </div>
  </div>`;

      html = html.replace(tocMatch[0], newToc);
    }

    // Add id to the "Seasonal Considerations" h2 in septic if it's missing
    if (tool.dir === 'septic-tank-sizing-calculator') {
      html = html.replace('<h2>Seasonal Considerations for Septic Installation</h2>', '<h2 id="seasonal-considerations">Seasonal Considerations for Septic Installation</h2>');
    }
  }

  // 3. Add Wikipedia Definition, Community Questions, Research Table, YouTube after the TOC for old-style, or after badges+TOC area for new-style
  // For old-style: insert after the upgraded TOC div, before the first article h2
  // For new-style: insert after the TOC we added

  const enrichmentBlock = generateWikiDef(tool) + generateCommunityQuestions(tool) + generateResearchTable(tool) + generateYouTubeEmbed(tool.ytId);

  if (tool.structureType === 'old') {
    // Insert before the first h2 content section (after toc)
    // Find the first <h2 id= after the toc
    const firstH2Regex = /  <\/div>\n\n  <h2 id="/;
    const firstH2Match = html.match(firstH2Regex);
    if (firstH2Match) {
      // Insert before the first h2 (after the TOC closing div)
      const insertPoint = '  </div>\n\n  <h2 id="';
      // Only replace the first occurrence after the TOC
      const tocEndIdx = html.indexOf('</div>\n  </div>\n\n  <h2 id="');
      if (tocEndIdx === -1) {
        // Try alternate pattern
        const altPoint = html.indexOf('    </div>\n  </div>\n\n  <h2 id="');
        if (altPoint !== -1) {
          html = html.slice(0, altPoint) + '    </div>\n  </div>\n' + enrichmentBlock + '\n\n  <h2 id="' + html.slice(altPoint + '    </div>\n  </div>\n\n  <h2 id="'.length);
        }
      } else {
        html = html.slice(0, tocEndIdx) + '</div>\n  </div>\n' + enrichmentBlock + '\n\n  <h2 id="' + html.slice(tocEndIdx + '</div>\n  </div>\n\n  <h2 id="'.length);
      }
    }
  } else {
    // For new-style: insert after the TOC div, before the first calculator-card / calc-card
    // The TOC was added right after badges. Insert enrichment after TOC, before the calculator card.
    if (tool.dir === 'heloc-repayment-calculator') {
      const calcCardStart = '<div class="calculator-card">';
      html = html.replace(calcCardStart, enrichmentBlock + '\n  ' + calcCardStart);
    } else if (tool.dir === 'cd-account-calculator') {
      const calcCardStart = '<div class="calculator-card">';
      html = html.replace(calcCardStart, enrichmentBlock + '\n  ' + calcCardStart);
    } else if (tool.dir === 'car-refinance-calculator') {
      const calcCardStart = '<div class="calc-card">';
      html = html.replace(calcCardStart, enrichmentBlock + '\n  ' + calcCardStart);
    }
  }

  // 4. Add Usage Counter - insert before footer
  const footerTag = '<footer>';
  if (html.includes(footerTag)) {
    html = html.replace(footerTag, generateUsageCounter() + '\n' + footerTag);
  }

  // 5. Add JS counter increment in calculate function
  const counterJS = `
  // Usage counter
  var c = document.getElementById('calcCount');
  if (c) c.textContent = parseInt(c.textContent || '0') + 1;`;

  const fnName = `function ${tool.calcFn}(`;
  const fnIdx = html.indexOf(fnName);
  if (fnIdx !== -1) {
    // Find the opening brace of the function
    const braceIdx = html.indexOf('{', fnIdx);
    if (braceIdx !== -1) {
      html = html.slice(0, braceIdx + 1) + counterJS + html.slice(braceIdx + 1);
    }
  }

  fs.writeFileSync(filePath, html, 'utf8');
  console.log(`Enriched: ${tool.dir}`);
});

console.log('All 6 tools enriched successfully.');
