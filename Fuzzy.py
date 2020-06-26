"""
** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** //***********************************************************************

	This file is part of KEEL-software, the Data Mining tool for regression,
	classification, clustering, pattern mining and so on.

	Copyright (C) 2004-2010

	F. Herrera (herrera@decsai.ugr.es)
    L. S谩nchez (luciano@uniovi.es)
    J. Alcal谩-Fdez (jalcala@decsai.ugr.es)
    S. Garc铆a (sglopez@ujaen.es)
    A. Fern谩ndez (alberto.fernandez@ujaen.es)
    J. Luengo (julianlm@decsai.ugr.es)

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see http://www.gnu.org/licenses/

**********************************************************************/
"""


# <p>This class contains the representation of a fuzzy value</p>
# '''
#  * @author Written by Alberto Fern谩ndez (University of Granada) 16/10/2007
#  * @version 1.0
#  * @since JDK1.5
# '''
class Fuzzy:
    # Default constructor
    x0 = None
    x1 = None
    x3 = None
    y = None
    name = ""
    label = None

    def __init__(self):
        x0 = None
        x1 = None
        x3 = None
        # print("init of Fuzzy Class ")

    # * If fuzzyfies a crisp value
    # * @param X double The crips value
    # * @return double the degree of membership
    # */

    def setX(self, X):
        # print("Set Fuzzy X method begin ......")
        # print("X = " +str(X)+" ,self.x0 = "+str(self.x0)+" ,self.x1 = "+str(self.x1)+", self.x3 = " + str(self.x3))
        if (X <= self.x0) or (X >= self.x3):  # /* If X is not in the range of D, the */
            # print("(X <= self.x0) or (X >= self.x3)")
            return 0.0  # /* membership degree is 0 */

        if X < self.x1:
            # print("X <  self.x1")
            return (X - self.x0) * (self.y / (self.x1 - self.x0))

        if X > self.x1:
            # print("X > self.x1")
            return (self.x3 - X) * (self.y / (self.x3 - self.x1))

        return self.y

        # /**
        #   * It makes a copy for the object
        #   * @return Fuzzy a copy for the object
        #   */

    def clone(self):
        d = Fuzzy()
        d.x0 = self.x0
        d.x1 = self.x1
        d.x3 = self.x3
        d.y = self.y
        d.name = self.name
        d.label = self.label
        return d
