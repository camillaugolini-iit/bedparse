import unittest
import bedparse

class KnownValues(unittest.TestCase):
    known_promoters = ( 
            (["chr1", 1000, 2000, "Name", 0, "+"], ["chr1", 500, 1500, "Name"]),
            (["chr1", 1000, 2000, "Name", 0, "-"], ["chr1", 1500, 2500, "Name"]),
            (["chr1", 100, 200, "Name", 0, "+"], ["chr1", 0, 600, "Name"]),
            (["chr1", 100, 200, "Name", 0, "-"], ["chr1", 0, 700, "Name"])
            )
    known_promoters100 = ( 
            (["chr1", 1000, 2000, "Name", 0, "+"], ["chr1", 900, 1100, "Name"]),
            (["chr1", 1000, 2000, "Name", 0, "-"], ["chr1", 1900, 2100, "Name"]),
            (["chr1", 50, 100, "Name", 0, "+"], ["chr1", 0, 150, "Name"]),
            (["chr1", 10, 80, "Name", 0, "-"], ["chr1", 0, 180, "Name"])
            )
    known_promotersUnstranded= ( 
            (["chr1", 1000, 2000, "Name", 0, "+"], ["chr1", 500, 1500, "Name"]),
            (["chr1", 1000, 2000, "Name", 0, "-"], ["chr1", 500, 1500, "Name"]),
            (["chr1", 1000, 2000, "Name", 0, "."], ["chr1", 500, 1500, "Name"])
            )

    badBed= (
            ["chr1", 1000, 200, "Name", 0, "+"],
            ["chr1", 1000, "a", "Name", 0, "+"],
            ["chr1", "a", 2000, "Name", 0, "+"],
            ["chr1", "1000", 2000, "Name", 0, "a"],
            ["chr1", 1000, 2000, "Name", 0, "+", 1000, 1000],
            ["chr1", 1000, 2000, "Name", 0, "+", 1000, 1000, ".", "a", "10,10,10,", "0,100,200,"],
            ["chr1", 1000, 2000, "Name", 0, "+", "a", 1000, ".", 3, "10,10,10,", "0,100,200,"],
            ["chr1", 1000, 2000, "Name", 0, "+", 1000, "a", ".", 3, "10,10,10,", "0,100,200,"],
            ["chr1", 1000, 2000, "Name", 0, "+", 1000, 900, ".", 3, "10,10,10,", "0,100,200,"],
            ["chr1", 1000, 2000, "Name", 0, "+", 100, 900, ".", 3, "10,10,10,", "0,100,200,"],
            ["chr1", 1000, 2000, "Name", 0, "+", 1500, 2001, ".", 3, "10,10,10,", "0,100,200,"],
            ["chr1", 1000, 2000, "Name", 0, "+", 1500, 2000, ".", 3, "10,10,10", "0,100,200,"],
            ["chr1", 1000, 2000, "Name", 0, "+", 1500, 2000, ".", 3, "10,10,10,", "0,100,200"],
            ["chr1", 1000, 2000, "Name", 0, "+", 1500, 2000, ".", 3, "10,10,10,10,", "0,100,200,"],
            ["chr1", 1000, 2000, "Name", 0, "+", 1500, 2000, ".", 3, "10,10,", "0,100,200,"],
            ["chr1", 1000, 2000, "Name", 0, "+", 1500, 2000, ".", 3, "10,10,10,", "0,100,"],
            ["chr1", 1000, 2000, "Name", 0, "+", 1500, 2000, ".", 3, "10,10,10,", "0,100,200,300,"],
            ["chr1", 1000, 2000, "Name", 0, "+", 1500, 2000, ".", 3, "10,10,a,", "0,100,200,"],
            ["chr1", 1000, 2000, "Name", 0, "+", 1500, 2000, ".", 3, "10,10,10,", "0,100,b,"]
            )

    known_introns =(
            (["chr1", 100, 420, "Name", 0, "+", 210, 310, ".", 4, "20,20,20,20,", "0,100,200,300,"], ["chr1", 120, 400, "Name", 0, "+", 120,120, ".", 3, "80,80,80,", "0,100,200,"]),
            (["chr1", 100, 420, "Name", 0, "-", 210, 310, ".", 4, "20,20,20,20,", "0,100,200,300,"], ["chr1", 120, 400, "Name", 0, "-", 120,120, ".", 3, "80,80,80,", "0,100,200,"]),
            (["chr1", 100, 420, "Name", 0, "-", 210, 310, ".", 1, "320,", "0,"], None),
            (["1", 100, 160, "Name", 0, "+"], None)
            )

    known_5pUTRs =(
            (["chr1", 100, 420, "Name", 0, "+", 210, 310, ".", 4, "20,20,20,20,", "0,100,200,300,"], ["chr1", 100, 210, "Name", 0, "+", 100,100, ".", 2, "20,10,", "0,100,"]),
            (["chr1", 100, 500, "Name", 0, "+", 200, 300, ".", 1, "400,", "0,"], ["chr1", 100, 200, "Name", 0, "+", 100,100, ".", 1, "100,", "0,"]),
            (["chr1", 100, 500, "Name", 0, "-", 200, 300, ".", 1, "400,", "0,"], ["chr1", 300, 500, "Name", 0, "-", 300,300, ".", 1, "200,", "0,"]),
            (["chr1", 100, 420, "Name", 0, "-", 210, 310, ".", 4, "20,20,20,20,", "0,100,200,300,"], ["chr1", 310, 420, "Name", 0, "-", 310,310, ".", 2, "10,20,", "0,90,"]),
            (["chr1", 100, 420, "Name", 0, "+", 100, 310, ".", 4, "20,20,20,20,", "0,100,200,300,"], None),
            # This is a case where the 5'UTR end on the last base of an exon
            (["1", 100, 160, "Name", 0, "+", 150,160, ".", 2, "10,10,", "0,50,"], ["1", 100, 110, "Name", 0, "+", 100,100, ".", 1, "10,", "0,"]),
            (["1", 100, 160, "Name!", 0, "+", 109,160, ".", 2, "10,10,", "0,50,"], ["1", 100, 109, "Name!", 0, "+", 100,100, ".", 1, "9,", "0,"])
            )

    known_3pUTRs =(
            (["chr1", 100, 420, "Name", 0, "+", 210, 310, ".", 4, "20,20,20,20,", "0,100,200,300,"], ["chr1", 310, 420, "Name", 0, "+", 310,310, ".", 2, "10,20,", "0,90,"]),
            (["chr1", 100, 500, "Name", 0, "-", 200, 300, ".", 1, "400,", "0,"], ["chr1", 100, 200, "Name", 0, "-", 100,100, ".", 1, "100,", "0,"]),
            (["chr1", 100, 500, "Name", 0, "+", 200, 300, ".", 1, "400,", "0,"], ["chr1", 300, 500, "Name", 0, "+", 300,300, ".", 1, "200,", "0,"]),
            (["chr1", 100, 420, "Name", 0, "-", 210, 310, ".", 4, "20,20,20,20,", "0,100,200,300,"], ["chr1", 100, 210, "Name", 0, "-", 100,100, ".", 2, "20,10,", "0,100,"]),
            (["chr1", 100, 420, "Name", 0, "+", 210, 420, ".", 4, "20,20,20,20,", "0,100,200,300,"], None),
            (["1", 100, 160, "Name", 0, "+", 100,110, ".", 2, "10,10,", "0,50,"], ["1", 150, 160, "Name", 0, "+", 150,150, ".", 1, "10,", "0,"])
            # This is a case where the 3'UTR starts on the first base of an exon
            #(["1", 44118849, 44135140, "ENST00000372299", 0, "+", 44118907, 44130756, ".", 4, "139,844,245,1903,", "0,10503,11662,14388,"], ["1", 44133237, 44135140, "ENST00000372299", 0, "+", 44133237, 44133237, ".", 1, "1903,", "0,"])
            )
    
    known_CDSs =(
            (["chr1", 100, 420, "Name", 0, "+", 210, 310, ".", 4, "20,20,20,20,", "0,100,200,300,"], ["chr1", 210, 310, "Name", 0, "+", 210, 310, ".", 2, "10,10,", "0,90,"]),
            (["chr1", 100, 420, "Name", 0, "-", 210, 310, ".", 4, "20,20,20,20,", "0,100,200,300,"], ["chr1", 210, 310, "Name", 0, "-", 210, 310, ".", 2, "10,10,", "0,90,"]),
            (["chr1", 100, 500, "Name", 0, "-", 200, 300, ".", 1, "400,", "0,"], ["chr1", 200, 300, "Name", 0, "-", 200,300, ".", 1, "100,", "0,"]),
            (["chr1", 100, 500, "Name", 0, "+", 200, 300, ".", 1, "400,", "0,"], ["chr1", 200, 300, "Name", 0, "+", 200,300, ".", 1, "100,", "0,"]),
            (["chr1", 100, 500, "Name", 0, "+", 100, 500, ".", 1, "400,", "0,"], ["chr1", 100, 500, "Name", 0, "+", 100, 500, ".", 1, "400,", "0,"]),
            (["chr17", 2420184, 2511835, "ENST00000574752", 0, "-", 2464312, 2502331, ".", 10, "412,174,167,90,70,143,141,200,128,77,", "0,546,16489,17924,21305,44023,53339,57501,82019,91574,"], ["chr17", 2464312, 2502331, "ENST00000574752", 0, "-", 2464312, 2502331, ".", 4, "38,141,200,128,", "0,9211,13373,37891,"])
            )
    
    known_CDS_ignoreCDSonly =(
            (["chr1", 100, 500, "Name", 0, "+", 100, 500, ".", 1, "400,", "0,"], None),
            (["chr1", 100, 500, "Name", 0, "-", 100, 500, ".", 1, "400,", "0,"], None)
            )

    known_bed12tobed6=(
            ['chr1', 14403, 29570, 'ENST00000488147.1', '0', '-', 29570, 29570, 0,11,'98,34,152,159,198,136,137,147,99,154,37,', '0,601,1392,2203,2454,2829,3202,3511,3864,10334,15130,'],
             [
                 ['chr1', 14403, 14501, 'ENST00000488147.1_Exon001', '0', '-'],
                 ['chr1', 15004, 15038, 'ENST00000488147.1_Exon002', '0', '-'],
                 ['chr1', 15795, 15947, 'ENST00000488147.1_Exon003', '0', '-'],
                 ['chr1', 16606, 16765, 'ENST00000488147.1_Exon004', '0', '-'],
                 ['chr1', 16857, 17055, 'ENST00000488147.1_Exon005', '0', '-'],
                 ['chr1', 17232, 17368, 'ENST00000488147.1_Exon006', '0', '-'],
                 ['chr1', 17605, 17742, 'ENST00000488147.1_Exon007', '0', '-'],
                 ['chr1', 17914, 18061, 'ENST00000488147.1_Exon008', '0', '-'],
                 ['chr1', 18267, 18366, 'ENST00000488147.1_Exon009', '0', '-'],
                 ['chr1', 24737, 24891, 'ENST00000488147.1_Exon010', '0', '-'],
                 ['chr1', 29533, 29570, 'ENST00000488147.1_Exon011', '0', '-']
            ])

    known_bed12tobed6_first=(
            (['chr1', 14403, 29570, 'ENST00000488147.1', '0', '+', 29570, 29570, 0,11,'98,34,152,159,198,136,137,147,99,154,37,', '0,601,1392,2203,2454,2829,3202,3511,3864,10334,15130,'],
                 ['chr1', 14403, 14501, 'ENST00000488147.1_Exon001', '0', '+']
            ),
            (['chr1', 14403, 29570, 'ENST00000488147.1', '0', '-', 29570, 29570, 0,11,'98,34,152,159,198,136,137,147,99,154,37,', '0,601,1392,2203,2454,2829,3202,3511,3864,10334,15130,'],
                 ['chr1', 29533, 29570, 'ENST00000488147.1_Exon011', '0', '-']
            ))

    known_bed12tobed6_last=(
            (['chr1', 14403, 29570, 'ENST00000488147.1', '0', '+', 29570, 29570, 0,11,'98,34,152,159,198,136,137,147,99,154,37,', '0,601,1392,2203,2454,2829,3202,3511,3864,10334,15130,'],
                 ['chr1', 29533, 29570, 'ENST00000488147.1_Exon011', '0', '+']
            ),
            (['chr1', 14403, 29570, 'ENST00000488147.1', '0', '-', 29570, 29570, 0,11,'98,34,152,159,198,136,137,147,99,154,37,', '0,601,1392,2203,2454,2829,3202,3511,3864,10334,15130,'],
                ['chr1', 14403, 14501, 'ENST00000488147.1_Exon001', '0', '-']
            ))

    def test_promoter100(self):
        '''promoters() should return correct promoters100 with known input'''
        for ((bed), (prom)) in self.known_promoters100:
            result = bedparse.bedline(bed).promoter(up=100, down=100)
            self.assertEqual(result, bedparse.bedline(prom))

    def test_promoterUnstranded(self):
        '''promoters() should return correct promotersUnstranded with known input'''
        for ((bed), (prom)) in self.known_promotersUnstranded:
            result = bedparse.bedline(bed).promoter(strand=0)
            self.assertEqual(result, bedparse.bedline(prom))

    def test_badBed(self):
        '''Bad BED lines should throw and exception'''
        for bed in self.badBed:
            self.assertRaises(bedparse.BEDexception, bedparse.bedline, bed)

    def test_introns(self):
        '''introns should return correct introns for know cases'''
        for ((bed), (introns)) in self.known_introns:
            result = bedparse.bedline(bed).introns()
            if(introns is None):
                self.assertEqual(result, None)
            else:
                self.assertEqual(result, bedparse.bedline(introns))

    def test_5pUTRs(self):
        '''fivePutr should return correct UTR for know cases'''
        for ((bed), (utr)) in self.known_5pUTRs:
            result = bedparse.bedline(bed).utr(which=5)
            if(utr is None):
                self.assertEqual(result, None)
            else:
                self.assertEqual(result, bedparse.bedline(utr))

    def test_3pUTRs(self):
        '''threePutr should return correct UTR for know cases'''
        for ((bed), (utr)) in self.known_3pUTRs:
            result = bedparse.bedline(bed).utr(which=3)
            if(utr is None):
                self.assertEqual(result, None)
            else:
                self.assertEqual(result, bedparse.bedline(utr))

    def test_CDSs(self):
        '''cds() should return correct CDSs for know cases'''
        for ((bed), (cds)) in self.known_CDSs:
            result = bedparse.bedline(bed).cds()
            self.assertEqual(result, bedparse.bedline(cds))
        for ((bed), (cds)) in self.known_CDS_ignoreCDSonly:
            result = bedparse.bedline(bed).cds(ignoreCDSonly=True)
            self.assertEqual(result, None)

    def test_bed12tobed6(self):
        '''bed12tobed6() should return correct BED6 records for know cases'''
        bed, res = self.known_bed12tobed6
        resBedline = []
        for i in res:
            resBedline.append(bedparse.bedline(i))
        result = bedparse.bedline(bed).bed12tobed6(appendExN=True)
        self.assertEqual(result,resBedline)

    def test_bed12tobed6_first(self):
        '''bed12tobed6(whichExon=first) should return correct BED6 records for know cases'''
        for ((bed), (res)) in self.known_bed12tobed6_first:
            res=bedparse.bedline(res)
            result = bedparse.bedline(bed).bed12tobed6(whichExon="first", appendExN=True)
            self.assertEqual(result,res)

    def test_bed12tobed6_last(self):
        '''bed12tobed6(whichExon=last) should return correct BED6 records for know cases'''
        for ((bed), (res)) in self.known_bed12tobed6_last:
            res=bedparse.bedline(res)
            result = bedparse.bedline(bed).bed12tobed6(whichExon="last", appendExN=True)
            self.assertEqual(result,res)

if __name__ == '__main__':
    unittest.main()
