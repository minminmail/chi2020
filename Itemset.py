# /**
#  * <p>Title: Itemset</p>
#  * <p>Description: This class contains the representation of a itemset</p>
#  * <p>Copyright: Copyright KEEL (c) 2007</p>
#  * <p>Company: KEEL </p>
#  * @author Jesus AlcalÃ¡ (University of Granada) 09/02/2011
#  * @version 1.0
#  * @since JDK1.6
#  */


class Itemset :
    itemset = []
  # int
    clas = None
  # double
    support = None
    supportRule = None

    # /**
    #  * Default constructor.
    #  * None attribute will be initialized.
    #  */
    def __init__:
        print("Itemset init ....")

    # * Builder
    # * @param clas Class

    def init_with_parameters(self,clas):
        self.itemset = []
        self.clas = clas
        self.support = 0
        self.supportRule = 0


    # * Clone
    # * @return Return a copy of the itemset
    def clone(self):
        d_itemset = Itemset(self.clas)
        for i in range(0, self.itemset.size()):
            d_itemset.add((self.itemset.get(i)).clone())
            d_itemset.clas = self.clas
            d_itemset.support = self.support;
            d_itemset.supportRule = self.supportRule

	return d_itemset


   # * Function to add an item to our itemset
   # * @param item Element to be added

    def add (self, item):
        self.itemset.add(item)


   # * It returns the item located in the given position of the itemset
   # * @param pos Position of the requested item into the itemset
   # * @return The requested item of the itemset

    def get (self, pos):
	  return self.itemset.get(pos)


   #  /**
   # * Function to remove the item located in the given position
   # * </p>
   # * @param pos Position of the requested item into the itemset
   # * @return The removed item of the itemset

    def remove (self, pos):
	  return (self.itemset.remove(pos))


   # * It returns the size of the itemset (the number of items it has)
   # * @return Number of items the itemset stores

    def size (self):
	  return self.itemset.size()

  # /**
  #  * <p>
  #  * It returns the support of the antecedent of the itemset
  #  * </p>
  #  * @return Support of the antecedent of the itemset
  #  */
    def getSupport(self):
        return self.support


     #   * It returns the support of the itemset for its related output class
     #   * @return Support of the itemset for its related output class

    def  getSupportClass(self):
	    return self.supportRule


   # * It returns the output class of the itemset
   # * @return output class of the itemset
    def getClas(self):
	    return self.clas


    # /**
    #  * Set the class with the value given as argument.
    #  * @param clas class given.
    #  */
    def setClas(self,clas):
	    self.clas = clas



   # * Function to check if an itemset is equal to another given
   # * @param a Itemset to compare with ours
   # * @return boolean true = they are equal, false = they aren't.



    def isEqual(self, a_itemset):
        i = None
        item = None

        if self.itemset.size() != a_itemset.size():
            return False
        if self.clas != a_itemset.getClas():
            return False
        for i in range (0, self.itemset.size()):
		    self.item = self.itemset.get(i)
		    if not self.item.isEqual(a_itemset.get(i)): return False
        return True







